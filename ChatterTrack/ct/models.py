from django.db import models
from django.contrib.auth.models import User
import datetime, pytz

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)

class TrackedUser(models.Model):
    twitter_id = models.CharField(max_length=60)
    twitter_id.primary_key = True
    screen_name = models.CharField(max_length=70)
    user = models.ForeignKey(Profile)
    track_until = models.DateTimeField(default=datetime.datetime.now(pytz.utc))
    followers_list = models.TextField()
    
    def __unicode__(self):
        return self.screen_name
    
class TrackedPhrase(models.Model):
    phrase = models.CharField(max_length=60)
    user = models.ForeignKey(Profile)
    tracking = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.phrase
        
class Stream(models.Model):
    tracked_user = models.ForeignKey(TrackedUser)
    stream_id = models.CharField(max_length=255)
    stream_hash = models.CharField(max_length=255)
    name = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.name
    
class Tweet(models.Model):
    text = models.CharField(max_length=150)
    stream = models.ForeignKey(Stream)
    category = models.CharField(max_length=63)
    category_confidence = models.FloatField()
    time = models.DateTimeField(default=datetime.datetime.now(pytz.utc))
    sentiment = models.FloatField()
    
    def __unicode__(self):
        return self.text
    
