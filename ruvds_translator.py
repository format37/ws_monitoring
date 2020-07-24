PORT = 8082
from aiohttp import web
import asyncio

async def call_check(request):
	return web.Response(text='ok',content_type="text/html")

rover_init()

app = web.Application()
app.router.add_route('GET', '/check',	call_check)

# Start aiohttp server
web.run_app(
    app,
    host='127.0.0.1',
    port=PORT,
)
