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
    user = models.ForeignKey(Profile)
    track_until = models.DateTimeField(default=datetime.datetime.now(pytz.utc))
    
    def __unicode__(self):
        return str(self.twitter_id)
    
class TrackedPhrase(models.Model):
    phrase = models.CharField(max_length=60)
    user = models.ForeignKey(Profile)
    tracking = models.BooleanField(default=True)
    
    def __unicode__(self):
        return str(self.phrase)
    
class Tweet(models.Model):
    text = models.CharField(max_length=150)
    TrackedUser = models.ForeignKey(TrackedUser)
    TrackedPhrase = models.ForeignKey(TrackedPhrase)
    TrackedPhrase.null = True
    time = models.DateTimeField(default=datetime.datetime.now(pytz.utc))
    
    def __unicode__(self):
        return str(self.text)
    
    
