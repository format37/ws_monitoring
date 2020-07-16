PORT = '8082'
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport
import asyncio
from aiohttp import web
import urllib

async def call_check(request):
	return web.Response(text='ok',content_type="text/html")

async def call_test(request):

	try:
	
		url		= request.rel_url.query['url']
		user	= urllib.parse.quote_plus(request.rel_url.query['user'])
		password= urllib.parse.quote_plus(request.rel_url.query['pass'])
		print('url',url)
		print('user',user)
		print('pass',password)
		session = Session()
		session.auth = HTTPBasicAuth(user, password)
		client = Client(url,transport=Transport(session=session))		
		answer = client.service.wsMonitorTest()
		
	except Exception as e:
		answer = 'Error: '+str(e)
		
	return web.Response(text=answer,content_type="text/html")

app = web.Application()
app.router.add_route('GET', '/check', call_check)
app.router.add_route('GET', '/test', call_test)

loop = asyncio.get_event_loop()
handler = app.make_handler()
f = loop.create_server(handler, port=PORT)
srv = loop.run_until_complete(f)

print('serving on', srv.sockets[0].getsockname())
try:
	loop.run_forever()
except KeyboardInterrupt:
	print("serving off...")
finally:
	loop.run_until_complete(handler.finish_connections(1.0))
	srv.close()