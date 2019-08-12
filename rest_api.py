import json
import time
import aiohttp_session
from aiohttp import web
from aiohttp_session import get_session,setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

async def handle(request):
    #response_obj = { 'status' : 'success' }
    #return web.Response(text=json.dumps(response_obj))
    session = await get_session(request)
    #print (session)
    #session['last_visit'] = time.time()
    session['last_visit'] = time.asctime( time.localtime(time.time()) )
    response_obj = { 'User logged in at ' : session['last_visit'] }
    print (aiohttp_session.SimpleCookieStorage())
    return web.Response(text=json.dumps(response_obj), status=200)


async def new_user(request):
    try:
        # happy path where name is set
        user = request.query['name']
        # Process our new user
        print("Creating new user with name: " , user)
        response_obj = { 'status' : 'success' }
        session = await get_session(request)
        session['last_visit'] = time.asctime( time.localtime(time.time()) )
        session['last_visit']='Welcome'+' '+user+' '+str(session['last_visit'])
        response_obj = { 'User' : session['last_visit'] }
        print (session['last_visit'])
        return web.Response(text=json.dumps(response_obj), status=200)

    except Exception as e:
        response_obj = { 'status' : 'failed', 'reason': str(e) }
        return web.Response(text=json.dumps(response_obj), status=500)

app = web.Application()
setup(app,
        EncryptedCookieStorage(b'Thirty  two  length  bytes  key.'))
app.router.add_get('/', handle)
app.router.add_post('/session', new_user)
web.run_app(app)

