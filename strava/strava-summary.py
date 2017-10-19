#!/usr/bin/python  
from datetime import datetime
from datetime import timedelta
#import time
from stravalib.client import Client
import tweepy

class Consumer:
    @property
    def client_code(self):
        return 'MC9ygBK2SmoBITB4gUeLz9lLk'

    @property
    def client_secret(self):
        return 'W8kW1VuLAxLOCmeMJjVurvi4tdyOn1n5ahfb44IVYX5yNx1Vcm'

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
    def TwitterName(self):
        return 'julesjoseph'
    @property
    def TwitterAccessCode(self):
        return '363734147-vtVb5BBsRe3G8wujBzxoi0uNdu1NA5VeSQ781den'

    @property
    def TwitterAccessSecret(self):
        return 'FEJUU6jv1iqxAUfBSk0oOAndXrEkJ0hlVB70bOqYgzxcM'

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

def sendsummary():
    stravaUser = StravaUser()
    consumer = Consumer()

    print("StravaUserId %d" % stravaUser.StravaUserId)
    print("StravaAccessToken %s" % stravaUser.StravaAccessToken)
    print("TwitterName %s" % stravaUser.TwitterName)
    print("TwitterAccessCode %s" % stravaUser.TwitterAccessCode)
    print("GetLastWeekStart %s" % GetLastWeekStart())
    print("GetLastWeekEnd %s" % GetLastWeekEnd())

    stravaClient = Client()
    stravaClient.access_token = stravaUser.StravaAccessToken
    athlete = stravaClient.get_athlete()
    print(athlete.email)

    #this method does not allow you to pass both before and after dates?
    #can we safely assume that 100 activities will cover at least one week?
    activities = stravaClient.get_activities(after=GetLastWeekStart(), limit=100)

    totalDistance = []
    totalTime = []
    rideCount = 0
    for activity in activities:
        if activity.start_date_local < GetLastWeekEnd():
            rideCount=rideCount+1
            totalDistance.append(float(activity.distance))
            totalTime.append(activity.moving_time)

    sdistance = sum(totalDistance)/1000
    stime = sum(totalTime, timedelta())
    saverage = sdistance/(float(stime.seconds)/float(3600))

    distanceText = '{:.2f}'.format(sdistance)
    averageSpeedText = '{:.2f}'.format(saverage)

    status = 'Last Week\'s #Strava: {rides} rides, {distance} km in {time} at {average} kmh'.format(rides=rideCount, distance=distanceText, time=stime, average=averageSpeedText)

    print(status)
    # create bot - veckostat twitter app
    #consumer key/consumer secret
    auth = tweepy.OAuthHandler(consumer.client_code, consumer.client_secret)

    #julesjoseph
    auth.set_access_token(stravaUser.TwitterAccessCode, stravaUser.TwitterAccessSecret)

    api = tweepy.API(auth)
    api.update_status(status)

if __name__ == '__main__':
    sendsummary()
