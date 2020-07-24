PORT = '8080'
from aiohttp import web
import asyncio

async def call_check(request):
	return web.Response(text='ok',content_type="text/html")

app = web.Application()
app.router.add_route('GET', '/check',	call_check)

web.run_app(
    app,
    port=PORT,
)
