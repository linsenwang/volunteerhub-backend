from flask import Flask, request, jsonify, Blueprint, url_for, session
from flask import redirect
from authlib.integrations.flask_client import OAuth
import time

auth = Blueprint('auth', __name__)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(auth)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@auth.route('/auth', methods=['POST'])
def auth():
    token = oauth.google.authorize_access_token()
    user_info = token['userinfo']
    # 判断是否为管理员
    user_info['is_admin'] = user_info['email'] in app.config['ADMIN_EMAILS']
    session['user'] = user_info
    return redirect('/')