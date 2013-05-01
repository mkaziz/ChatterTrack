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
def add(x,y):
    return x + y

@task()
def track(tracking_info):
    
    startTime = datetime.now()
    
    stream = TwitterStream(auth=OAuth(tracking_info["user"]["oauth_token"], tracking_info["user"]["oauth_secret"], settings.TWITTER_KEY, settings.TWITTER_SECRET))
    trackedUsers = TrackedUser.objects.all()
    trackedUsersString = ""
    
    """
    for tu in trackedUsers:
        trackedUsersString += tu.user_id + ","
    
    trackedUsersString = trackedUsersString[:-1] # get rid of comma
    iterator = stream.statuses.filter(users=trackedUsersString)
    """
    iterator = stream.statuses.filter(follow="1069205491", block=False)

    for tweet in iterator:
        if datetime.now() > tracking_info["track_until"]:
            break; 
        tweeter = None
        try:
            tweeter = TrackedUser.objects.get(twitter_id=tweet["user"]["id_str"])
        except TrackedUser.DoesNotExist:
            raise Exception("Tracked User does not exist is db")
            
        t = Tweet(text=tweet["text"], user = tweeter)
        t.save()
        
    return;
    
