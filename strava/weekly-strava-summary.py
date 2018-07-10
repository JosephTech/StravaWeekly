#!/usr/bin/python
from datetime import datetime
from datetime import timedelta
#import datetime
from stravalib.client import Client
import tweepy

class Consumer:
    @property
    def client_code(self):
        return 'xxx'

    @property
    def client_secret(self):
        return 'xxx'

class StravaUser:
    @property
    def StravaUserId(self):
		#julesjoseph
        return 108191

    @property
    def StravaAccessToken(self):
        access_token = Client().exchange_code_for_token(client_id=1237, client_secret='xxx', code='xxx')
        return access_token

    @property
    def StravaTwitterUser(self):
        return '@julesjoseph'

    @property
    def TwitterName(self):
        return 'veckostat'

    @property
    def TwitterAccessCode(self):
        #veckostat
        return 'xxx'

    @property
    def TwitterAccessSecret(self):
        #veckostat
        return 'xxx'

#date helper methods
def GetCurrentDate():
    return datetime.now().date()

def GetLastWeekStart():
    day = datetime.now().date()
    lastWeekStart = day - timedelta(days=day.weekday()) + timedelta(days=0, weeks=-1)
    return datetime(lastWeekStart.year, lastWeekStart.month, lastWeekStart.day, 0, 0, 0)

def GetLastWeekEnd():
    day = datetime.now().date()
    lastWeekEnd =  day - timedelta(days=day.weekday()) + timedelta(days=6, weeks=-1)
    return datetime(lastWeekEnd.year, lastWeekEnd.month, lastWeekEnd.day, 23, 59, 59)

def monday_test():
    current_day = datetime.today()
    weekday = current_day.weekday()
    if (weekday == 0):
        print("It's Monday - woohoo :)")
        send_summary()
    else:
        print("It's not Monday :(")
        send_summary()


def send_summary():
    stravaUser = StravaUser()
    consumer = Consumer()

    print("StravaUserId %d" % stravaUser.StravaUserId)
    print("StravaAccessToken %s" % stravaUser.StravaAccessToken)
    print("TwitterName %s" % stravaUser.StravaTwitterUser)
    print("TwitterAccessCode %s" % stravaUser.TwitterAccessCode)
    print("GetLastWeekStart %s" % GetLastWeekStart())
    print("GetLastWeekEnd %s" % GetLastWeekEnd())

    stravaClient = Client()
    stravaClient.access_token = stravaUser.StravaAccessToken
    athlete = stravaClient.get_athlete()
    print(athlete.email)
    stravaTwitterUser = stravaUser.StravaTwitterUser

    #this method does not allow you to pass both before and after dates?
    #can we safely assume that 100 activities will cover at least one week?
    activities = stravaClient.get_activities(after=GetLastWeekStart(), limit=100)

    totalDistance = []
    totalTime = []
    rideCount = 0
    #for activity in activities:
    #    if activity.start_date_local < GetLastWeekEnd():
    #        rideCount=rideCount+1
    #        totalDistance.append(float(activity.distance))
    #        totalTime.append(activity.moving_time)

    #sdistance = sum(totalDistance)/1000
    #stime = sum(totalTime, timedelta())
    #saverage = sdistance/(float(stime.seconds)/float(3600))

    #distanceText = '{:.2f}'.format(sdistance)
    #averageSpeedText = '{:.2f}'.format(saverage)

    distanceText = 100
    averageSpeedText = 25.0
    stime = 8
    rideCount = 10

    status = '{twitterUser} Last Week\'s #Strava: {rides} rides, {distance} km in {time} at {average} kmh'.format(rides=rideCount, distance=distanceText, time=stime, average=averageSpeedText, twitterUser=stravaTwitterUser)

    print(status)
    # create bot - veckostat twitter app
    #consumer key/consumer secret
    auth = tweepy.OAuthHandler(consumer.client_code, consumer.client_secret)

    #julesjoseph
    auth.set_access_token(stravaUser.TwitterAccessCode, stravaUser.TwitterAccessSecret)

    api = tweepy.API(auth)
    api.update_status(status)

if __name__ == '__main__':
    monday_test()
