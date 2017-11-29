#!/usr/bin/python
from datetime import *
#from datetime import timedelta
from stravalib.client import Client
import tweepy


#veckostat
class Consumer:
    @property
    def TwitterAccount(self):
        return 'veckostat'

    @property
    def client_code(self):
        #twitter
        return 'MC9ygBK2SmoBITB4gUeLz9lLk'

    @property
    def client_secret(self):
        #twitter
        return 'W8kW1VuLAxLOCmeMJjVurvi4tdyOn1n5ahfb44IVYX5yNx1Vcm'

    @property
    def TwitterAccessCode(self):
        #veckostat
        return '917308663181856769-UXVltPmN9ACDTX4lrKrsYVc4UOSyIEc'

    @property
    def TwitterAccessSecret(self):
        #veckostat
        return 'KwAM4a6DyoyKmjYcC50r2ox1C2n04jRtOaw7kdmWnxYwI'    



#julesjoseph
class StravaUser:
    @property
    def StravaUserId(self):
		#julesjoseph
        return 108191

    @property
    def StravaAccessToken(self):
        access_token = Client().exchange_code_for_token(client_id=1237, client_secret='c63852bf687d35e062f1414ee69c49fc9d523767', code='cda0c994a35137f6433e7e717af6bfbfc1eb0f8f')
        return access_token

    @property
    def TwitterAccount(self):
        return '@julesjoseph'






def send_summary():
    stravaUser = StravaUser()
    consumer = Consumer()


    stravaClient = Client()
    stravaClient.access_token = stravaUser.StravaAccessToken
    athlete = stravaClient.get_athlete()

    year_total = athlete.stats.ytd_ride_totals.distance.num/1000

    end_of_year = date(2017, 12, 31)
    current_date = date.today()
    remaining_days = (end_of_year - current_date).days
    remaining_distance = 10000 - year_total
    daily_target = remaining_distance/remaining_days
    weekly_target = remaining_distance/(remaining_days/7)

    
    
    status = '{0} #Strava ytd/goal: {1:.0f}/10000 - daily target: {2:.2f}km, weekly target: {3:.2f}km'.format(stravaUser.TwitterAccount, year_total, daily_target, weekly_target)

    print(status)
    # create bot - veckostat twitter app
    #consumer key/consumer secret
    auth = tweepy.OAuthHandler(consumer.client_code, consumer.client_secret)

    #veckostat
    auth.set_access_token(consumer.TwitterAccessCode, consumer.TwitterAccessSecret)

    api = tweepy.API(auth)
    api.update_status(status)

if __name__ == '__main__':
    send_summary()