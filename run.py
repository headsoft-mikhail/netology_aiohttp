from aiohttp import web
from app import app
import routes


if __name__ == '__main__':
    web.run_app(app)
