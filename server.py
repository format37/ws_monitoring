from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport

async def call_check(request):
	return web.Response(text='ok',content_type="text/html")

async def call_check(request):
	url		= request.rel_url.query['url'] # 'http://10.2.4.141/test1c5/ws/ws1.1cws?wsdl'
	user	= request.rel_url.query['user'] # "ws1user"
	password= request.rel_url.query['pass'] # "pass"
	session = Session()
	session.auth = HTTPBasicAuth(user, password)
	client = Client(url,transport=Transport(session=session))

	answer = 'no data'
	
	try:
		
		answer = client.service.wsMonitorTest()
		
	except Exception as e:
		answer = 'Error: '+str(e)
		
	return web.Response(text=answer,content_type="text/html")

app = web.Application()
app.router.add_route('GET', '/check', call_check)
app.router.add_route('GET', '/test', call_test)

loop = asyncio.get_event_loop()
handler = app.make_handler()
f = loop.create_server(handler, port='8082')
srv = loop.run_until_complete(f)

print('serving on', srv.sockets[0].getsockname())
try:
	loop.run_forever()
except KeyboardInterrupt:
	print("serving off...")
finally:
	loop.run_until_complete(handler.finish_connections(1.0))
	srv.close()