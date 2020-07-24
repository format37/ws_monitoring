PORT = 8082
from aiohttp import web
import asyncio

async def call_check(request):
	return web.Response(text='ok',content_type="text/html")

app = web.Application()
app.router.add_route('GET', '/check',	call_check)

# Start aiohttp server
web.run_app(
    app,
    host='195.133.145.105',
    port=PORT,
)
