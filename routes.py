from aiohttp import web
from app import app
from views import test, UserView, PostView

app.add_routes(
    [
        web.get('/', test),
        web.post('/user', UserView),
        web.get('/user/{user_id}', UserView),
        web.post('/post', PostView),
        web.get('/post/{post_id}', PostView),
        web.put('/post/{post_id}', PostView),
        web.delete('/post/{post_id}', PostView),

    ]
)
