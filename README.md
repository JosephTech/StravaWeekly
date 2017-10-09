# veckostatistik

https://www.strava.com/oauth/authorize?client_id=458&response_type=code&redirect_uri=http://feedmyride.net/token_exchange&approval_prompt=force


class StravaLoginHandler(BaseHandler):
    def get(self):

        strava_login_uri = "https://www.strava.com/oauth/authorize?client_id="+strava_client_id+"&response_type=code&redirect_uri=http://feedmyride.net/token_exchange&approval_prompt=force"
        self.redirect(strava_login_uri)
        
        
class OauthCallbackHandler(BaseHandler):
    def get(self):

        mycode = self.get_argument("code")

        strava_token_uri = 'https://www.strava.com/oauth/token'
        params = {
          'client_id' : strava_client_id,
          'client_secret' : strava_client_secret,
          'code' : mycode,
        }
        
  (r"/token_exchange", OauthCallbackHandler),        
