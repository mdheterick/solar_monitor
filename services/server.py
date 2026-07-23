#! /usr/bin/python3 -u
from aiohttp import web
import env

from solar import api as solar_api

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "*"
}


def index(request):
    return web.FileResponse(env.services_dir + 'client/dist/index.html')

app = web.Application()
app.add_routes([
    web.get("/", index),
    *solar_api.routes,
    web.static("/", env.services_dir + "client/dist/"),
])

web.run_app(app)
