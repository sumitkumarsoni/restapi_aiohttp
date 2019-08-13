import json
import time
from aiohttp import web
from aiohttp_session import get_session,setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

class build_api(object):

        async def handle(self,request):

            """ Method handles the GET requests """
            session = await get_session(request)
            session['last_visit'] = time.asctime( time.localtime(time.time()) )
            response_obj = { 'User logged in at ' : session['last_visit'] }
            return web.Response(text=json.dumps(response_obj), status=200)


        async def new_user(self,request):
            """ Method  handles the POST requests """
            try:
                user = request.query['name']
                # Process our new user
                print("Creating new user with name: " , user)
                response_obj = { 'status' : 'success' }
                session = await get_session(request)
                session['last_visit'] = time.asctime( time.localtime(time.time()) )
                session['last_visit']='Welcome'+' '+user+' '+str(session['last_visit'])
                response_obj = { 'User' : session['last_visit'] }
                return web.Response(text=json.dumps(response_obj), status=200)

            except Exception as e:
                response_obj = { 'status' : 'failed', 'reason': str(e) }
                return web.Response(text=json.dumps(response_obj), status=500)

if __name__ == "__main__":

        app = web.Application()
        setup(app,EncryptedCookieStorage(b'Thirty  two  length  bytes  key.'))   # required setup to create session 
        api = build_api()
        app.router.add_get('/', api.handle)
        app.router.add_post('/session', api.new_user)
        web.run_app(app)