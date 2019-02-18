#!/usr/bin/python
from datetime import *
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
        return 'xxxx'

    @property
    def client_secret(self):
        #twitter
        return 'xxx'

    @property
    def TwitterAccessCode(self):
        #veckostat
        return 'xxx'

    @property
    def TwitterAccessSecret(self):
        #veckostat
        return 'xxx'



#julesjoseph
class StravaUser:
    @property
    def StravaUserId(self):
		#julesjoseph
        return 99999

    @property
    def StravaAccessToken(self):
        access_token = Client().exchange_code_for_token(client_id=9999, client_secret='xxx', code='xxx')
        return access_token

    @property
    def TwitterAccount(self):
        return '@julesjoseph'






def send_summary():
    stravaUser = StravaUser()
    consumer = Consumer()


    currentYear = 2018
    stravaClient = Client()
    stravaClient.access_token = stravaUser.StravaAccessToken
    athlete = stravaClient.get_athlete()

    #year_target = 10000
    year_to_date_distance = athlete.stats.ytd_ride_totals.distance.num/1000

    #end_of_year = date(currentYear, 12, 31)
    start_of_year = date(currentYear, 1, 1)

    current_date = date.today()
    days_to_date = (current_date - start_of_year).days
    average_daily_distance = year_to_date_distance/days_to_date

    #remaining_days = (end_of_year - current_date).days
    projected_distance_for_year = 365 * average_daily_distance


    #remaining_distance = year_target - year_to_date_distance
    #daily_target = remaining_distance/remaining_days
    #weekly_target = remaining_distance/(remaining_days/7)

    #status = '{0} #Strava ytd/goal: {1:.0f}/10000 - daily target: {2:.2f}km, weekly target: {3:.2f}km'.format(stravaUser.TwitterAccount, year_to_date_distance, daily_target, weekly_target)
    status = '{0} #Strava projected distance for {1}: {2:,.2f} km based on current average of {3:.2f} km/day'.format(stravaUser.TwitterAccount, currentYear, projected_distance_for_year, average_daily_distance)

    # create bot - veckostat twitter app
    #consumer key/consumer secret
    auth = tweepy.OAuthHandler(consumer.client_code, consumer.client_secret)

    #veckostat
    auth.set_access_token(consumer.TwitterAccessCode, consumer.TwitterAccessSecret)

    api = tweepy.API(auth)
    api.update_status(status)

def monday_test():
    current_day = datetime.today()
    weekday = current_day.weekday()
    #if (weekday == 0):
    print("It's Monday - woohoo :)")
    send_summary()
    #else:
    #    print("It's not Monday :(")

if __name__ == '__main__':
    monday_test()
