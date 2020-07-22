#PORT = '8082'
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport
import asyncio
from aiohttp import web
import urllib
import ssl

SCRIPT_PATH	= '/home/dvasilev/projects/ws_monitoring/'
WEBHOOK_PORT = 80  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = SCRIPT_PATH+'webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = SCRIPT_PATH+'webhook_pkey.pem'  # Path to the ssl private key

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
		if answer == True:
			answer = '1'
		else:
			answer = '0'			
		
	except Exception as e:
		answer = 'Error: '+str(e)
		
	return web.Response(text=answer,content_type="text/html")

app = web.Application()
app.router.add_route('GET', '/check', call_check)
app.router.add_route('GET', '/test', call_test)

# Build ssl context
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

# Start aiohttp server
web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
#    ssl_context=context,
)

'''
loop = asyncio.get_event_loop()
handler = app.make_handler()
f = loop.create_server(handler, port=PORT, ssl_context=context,)
srv = loop.run_until_complete(f)

print('serving on', srv.sockets[0].getsockname())
try:
	loop.run_forever()
except KeyboardInterrupt:
	print("serving off...")
finally:
	loop.run_until_complete(handler.finish_connections(1.0))
	srv.close()
'''
