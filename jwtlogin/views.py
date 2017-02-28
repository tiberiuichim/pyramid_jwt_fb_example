from __future__ import print_function
from cornice import Service
from pyramid.view import view_config
import jwt
import requests


@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    return {'project': 'jwtlogin'}


def fb_authenticate(user_id, access_token):
    url = "https://graph.facebook.com/v2.8/me"
    data = {
        'fields': 'id,name',
        'access_token': access_token
    }
    resp = requests.get(url, params=data)
    fbdata = resp.json()

    if fbdata['id'] == user_id:
        return user_id


@view_config(name='login', request_method='POST', renderer='json')
def login(request):
    user_id = request.POST['user_id']
    access_token = request.POST['access_token']
    user_id = fb_authenticate(user_id, access_token)
    request.response.headers['Access-Control-Allow-Origin'] = '*'
    if user_id:
        return {
            'result': 'ok',
            'token': request.create_jwt_token(user_id)
        }
    else:
        return {
            'result': 'error'
        }


token_exchange = Service(name='token_exchange',
                         path='/token-exchange',
                         description='FB to JWT token exchange and login.',
                         cors_origins=('*',),
                         cors_max_age=3600
                         )


@token_exchange.post()
def exchange(request):
    d = request.json_body
    user_id = d['user_id']
    access_token = d['access_token']
    user_id = fb_authenticate(user_id, access_token)
    # request.response.headers['Access-Control-Allow-Origin'] = '*'
    if user_id:
        return {
            'result': 'ok',
            'token': request.create_jwt_token(user_id)
        }
    else:
        return {
            'result': 'error'
        }


@view_config(route_name='check-token',
             request_method='POST',
             renderer='templates/check-token.pt')
def check_token(request):
    jwt_token = request.POST['jwt_token']
    claims = jwt.decode(jwt_token,
                        request.registry.settings['jwt.private_key'])
    return {'claims': claims}


secondpage = Service(name='secondpage',
                     path='/second-page',
                     description='Second view page',
                     cors_origins=('*',),
                     cors_max_age=3600
                     )


@secondpage.get()
def something_protected(request):
    return {
        'text': 'hello world'
    }
