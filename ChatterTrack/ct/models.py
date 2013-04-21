from django.db import models

# Create your models here.
class User(models.Model):
  user_id = models.CharField(max_length=60)
  user_id.primary_key = True;
  oauth_token = models.CharField(max_length=256)
  oauth_secret = models.CharField(max_length=256)
  screen_name = models.CharField(max_length=60)
