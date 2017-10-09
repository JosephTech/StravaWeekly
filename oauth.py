import json

from rauth import OAuth1Service
from flask import current_app, url_for, request, redirect, session

class OAuthSignIn(object):
    def __init__(self):
        self.provider_name = 'twitter'
        credentials = current_app.config['OAUTH_CREDENTIALS']['twitter']
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/')


    def authorize(self):
        request_token = self.service.get_request_token(
            params={'oauth_callback': self.get_callback_url()}
        )
        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    def get_callback_url(self):
        return url_for('oauth_callback', provider='twitter',
                       _external=True)

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return None, None, None

        oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']}
        )        
        me = oauth_session.get('account/verify_credentials.json').json()

        social_id = 'twitter$' + str(me.get('id'))
        username = me.get('screen_name')
        return social_id, username, None                         

