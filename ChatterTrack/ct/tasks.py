# celery
from celery import task

# twitter
from twitter import *

# django
from ct.models import *
from django.conf import settings

# generic python imports
from datetime import datetime, timedelta
import pytz

@task()
def track(tracking_info):
    
    stream = TwitterStream(auth=OAuth(tracking_info["user"]["oauth_token"], tracking_info["user"]["oauth_secret"], settings.TWITTER_KEY, settings.TWITTER_SECRET))
    
    iterator = stream.statuses.filter(follow=getTrackedUsersString(), block=False)
    
    for tweet in iterator:
        
        if tweet is None or "user" not in tweet or "text" not in tweet:
            trackedUsers = TrackedUser.objects.filter(track_until__gte=datetime.now(pytz.utc))
            
            if len(trackedUsers) == 0:
                return
            else:
                continue
  
        tweeter = None
        try:
            tweeter = TrackedUser.objects.get(twitter_id=tweet["user"]["id_str"])
        except TrackedUser.DoesNotExist:
            print "Tracked User does not exist"
            continue
            #raise Exception("Tracked User does not exist is db")
        
        if datetime.now(pytz.utc) > tweeter.track_until: 
            trackedUsersString = getTrackedUsersString()
            if len(trackedUsersString) == 0:
                return
            iterator = stream.statuses.filter(follow=trackedUsersString, block=False)
            continue
        
        print tweet["text"]
            
        t = Tweet(text=tweet["text"], TrackedUser=tweeter)
        t.save()
        
    return; 
    
def getTrackedUsersString():
    
    trackedUsers = TrackedUser.objects.all()
    
    trackedUsersString = ""

    for tu in trackedUsers:
        #print "checking: " + tu.twitter_id + " tracked until: " + str(tu.track_until)
        if datetime.now(pytz.utc) < tu.track_until:
            trackedUsersString += tu.twitter_id + ","
    
    trackedUsersString = trackedUsersString[:-1] # get rid of last comma
    
    print trackedUsersString
    
    return trackedUsersString
