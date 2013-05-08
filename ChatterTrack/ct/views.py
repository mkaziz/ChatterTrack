# Django imports
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ct.models import *
from ct.forms import TrackForm
from ct.tasks import track as track_task

# python imports
import json, requests, twitter, urlparse
from urllib import quote, urlencode
import oauth2 as oauth
import cgi
from datetime import datetime, timedelta
from twitter import *
import random
import datasift

# twitter api urls
request_token_url = 'http://api.twitter.com/oauth/request_token'
access_token_url = 'http://api.twitter.com/oauth/access_token'
authenticate_url = 'http://api.twitter.com/oauth/authenticate'

def createError(msg):
    response_data = { "error" : -1, "message" : msg }
    return HttpResponseBadRequest(content=json.dumps(response_data), content_type="application/json")

def index(request):
    response_data = { "error" : -1, "message" : "test" }
    return render(request, "index.html")
  #return HttpResponse(content=json.dumps(response_data), content_type="application/json")

def login(request):
    return render(request, "login.html")

@csrf_exempt
def datasiftLog(request):
    response_data = { "success" : True }
    return HttpResponse(content=json.dumps(response_data), content_type="application/json")

@login_required(login_url='/ct/login/') 
def track(request):
    form = None
    if (request.method == "POST"):
        form = TrackForm(request.POST)
        if form.is_valid():
            
            cd = form.cleaned_data
            twitterHandle = cd["twitter_handle"]
            timeToTrack = cd["time_to_track"]
            
            profile = Profile.objects.get(user=request.user)
            
            twitterObj = Twitter(auth=OAuth(profile.oauth_token, profile.oauth_secret, settings.TWITTER_KEY, settings.TWITTER_SECRET))
            twitterUser = twitterObj.users.show(screen_name=twitterHandle)
            
            listOfFollowers = twitterObj.followers.ids(screen_name=twitterHandle)["ids"]
            #subsetOfFollowers = random.sample(listOfFollowers, (1000 if len(listOfFollowers) > 1000 else len(listOfFollowers)))
            
            trackedUsersString = ""
            
            for follower in listOfFollowers:
                    
                try:
                    tu = TrackedUser.objects.get(twitter_id=str(follower))
                    tu.track_until = datetime.now()+timedelta(minutes=int(timeToTrack))
                    tu.save()
                except TrackedUser.DoesNotExist:
                    tu = TrackedUser(twitter_id=str(follower), user=profile, track_until=datetime.now()+timedelta(minutes=int(timeToTrack)))
                    tu.save()
                trackedUsersString += tu.twitter_id + ","
                
            trackedUsersString = trackedUsersString[:-1] # get rid of last comma
            
            dsUser = datasift.User(settings.DATASIFT["username"], settings.DATASIFT["api_key"])
            cdsl = "twitter.user.id in ["+trackedUsersString+"]"
            streamDef = dsUser.create_definition(cdsl)
            
            pushDef = dsUser.create_push_definition()
            pushDef.set_output_type("http")
            pushDef.set_output_param("delivery_frequency", 60)
            pushDef.set_output_param("max_size", 1000000)
            pushDef.set_output_param("url", "http://ec2-54-244-189-248.us-west-2.compute.amazonaws.com/ct/datasiftLog/")
            
            sub = pushDef.subscribe_definition(streamDef, twitterHandle)
            
            """
            user = User(settings.DATASIFT["username"], settings.DATASIFT["api_key"]
            tracking_info = {
                "user" : {
                    "oauth_token" : profile.oauth_token,
                    "oauth_secret" : profile.oauth_secret
                }
            }
            
            track_task.delay(tracking_info)
            #track_task(tracking_info)
            """
            return createError("form received")
    else:
        form = TrackForm()
    return render(request, "track.html", {'form' : form })

def twitter_login(request):
    
    consumer = oauth.Consumer(settings.TWITTER_KEY, settings.TWITTER_SECRET)
    client = oauth.Client(consumer)
    
    resp, content = client.request(request_token_url, "POST", body="oauth_callback=http://ec2-54-244-189-248.us-west-2.compute.amazonaws.com/ct/twitter_authenticated/")
    
    if resp['status'] != '200':
        raise Exception("Invalid response from Twitter.")

    # Step 2. Store the request token in a session for later use.
    request.session['request_token'] = dict(cgi.parse_qsl(content))

    # Step 3. Redirect the user to the authentication URL.
    url = "%s?oauth_token=%s" % (authenticate_url,
        request.session['request_token']['oauth_token'])

    return HttpResponseRedirect(url)

def twitter_authenticated(request):
    
    consumer = oauth.Consumer(settings.TWITTER_KEY, settings.TWITTER_SECRET)
    token = oauth.Token(request.session['request_token']['oauth_token'], request.session['request_token']['oauth_token_secret'])
    
    if 'oauth_verifier' in request.GET:
        token.set_verifier(request.GET['oauth_verifier'])
        
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    
    if resp['status'] != '200':
        raise Exception("Invalid response from Twitter.")

    access_token = dict(cgi.parse_qsl(content))
    
    try:
        user = User.objects.get(username=access_token['screen_name'])
    except User.DoesNotExist:
        user = User.objects.create_user(username=access_token['screen_name'], password=access_token['oauth_token_secret'])
        user.set_password(access_token['oauth_token_secret'])
        user.save()
        # Save our permanent token and secret for later.
        profile = Profile()
        profile.user = user
        profile.oauth_token = access_token['oauth_token']
        profile.oauth_secret = access_token['oauth_token_secret']
        profile.save()

    user = authenticate(username=access_token['screen_name'], password=access_token['oauth_token_secret'])
    
    auth_login(request, user)
    request.session["screen_name"] = access_token['screen_name']

    return HttpResponseRedirect('/ct/')
