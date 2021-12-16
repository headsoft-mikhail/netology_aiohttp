from aiohttp import web
from asyncpg import exceptions as pg_exceptions
from models import User, Post
import hashlib
from config import SALT
import validator
from pydantic.error_wrappers import ValidationError


async def test(request):
    return web.Response(text='Status: OK')


class UserView(web.View):
    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        user = await User.get(user_id)
        if user is not None:
            return web.json_response(user.to_dict())
        else:
            raise web.HTTPNotFound(reason='User with requested id not found')

    async def post(self):
        user_data = await self.request.json()
        try:
            user_data = validator.UserCreateValidator(**user_data).dict()
            user_email = user_data['email']
            user_name = user_data.get('name')
            raw_password = user_data['password']
            user_password = hashlib.md5(f'{raw_password}{SALT}'.encode()).hexdigest()
            new_user = await User.create(email=user_email,
                                         name=user_name,
                                         password=user_password)
            return web.json_response(new_user.to_dict())
        except ValidationError:
            raise web.HTTPBadRequest()
        except pg_exceptions.UniqueViolationError:
            raise web.HTTPForbidden(reason='User with the given email already exists')


class PostView(web.View):
    async def get(self):
        post_id = int(self.request.match_info['post_id'])
        post = await Post.get(post_id)
        if post is not None:
            return web.json_response(post.to_dict())
        else:
            raise web.HTTPNotFound(reason='Post with requested id not found')

    async def post(self):
        post_data = await self.request.json()
        try:
            post_data = validator.PostCreateValidator(**post_data).dict()
            post_title = post_data['title']
            post_text = post_data.get('text')
            owner_id = post_data.get('owner_id')
            new_post = await Post.create(title=post_title,
                                         text=post_text,
                                         owner_id=owner_id)
            return web.json_response(new_post.to_dict())
        except ValidationError:
            raise web.HTTPBadRequest()

    async def put(self):
        post_data = await self.request.json()
        try:
            post_data = validator.PostUpdateValidator(**post_data).dict()
            post_title = post_data.get('title', None)
            post_text = post_data.get('text', None)
            post_id = int(self.request.match_info['post_id'])
            post = await Post.get(post_id)
            if post is not None:
                if post_title is None:
                    post_title = post.title
                if post_text is None:
                    post_text = post.text
                await post.update(title=post_title, text=post_text).apply()
                return web.json_response(post.to_dict())
            else:
                raise web.HTTPNotFound(reason='Post with requested id not found')
        except ValidationError:
            raise web.HTTPBadRequest()

    async def delete(self):
        post_id = int(self.request.match_info['post_id'])
        post = await Post.get(post_id)
        if post is not None:
            await post.delete()
            raise web.HTTPNoContent(reason='Successfully deleted')
        else:
            raise web.HTTPNotFound(reason='Post with requested id not found')
