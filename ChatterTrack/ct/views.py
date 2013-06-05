# Django imports
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ct.models import *
from ct.forms import *
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
from sys import stderr

# logging
import logging
log = logging.getLogger('ct')

# twitter api urls
request_token_url = 'http://api.twitter.com/oauth/request_token'
access_token_url = 'http://api.twitter.com/oauth/access_token'
authenticate_url = 'http://api.twitter.com/oauth/authenticate'

def createError(msg):
    response_data = { "error" : -1, "message" : msg }
    return HttpResponseBadRequest(content=json.dumps(response_data), content_type="application/json")

def index(request):
    
    profileName = request.GET.get("profile","")
     
    if (profileName == ""):
        return createError("No Profile Name passed as parameter")
    
    try:
        profile = Profile.objects.get(user=User.objects.get(username=profileName))
    except Profile.DoesNotExist:
        return createError("Twitter profile does not exist for user: " + profileName)
    except User.DoesNotExist:
        return createError("Invalid Profile name: " + profileName)
        
    trackedUsers = TrackedUser.objects.filter(user=profile)
    
    results = []
    for tu in trackedUsers:
        streams = Stream.objects.filter(tracked_user=tu)
        for stream in streams:
            results.append(stream)
     
    return render(request, "index.html", {"streams" : results })
  #return HttpResponse(content=json.dumps(response_data), content_type="application/json")

def login(request):
    return render(request, "login.html")

def analyzeStream(request):
    
    streamId = request.GET.get("stream_id","")
    categoryConfidence = request.GET.get("category_confidence",0.0)
    
    stream = None
    try:
        stream = Stream.objects.get(stream_id=streamId)
    except Stream.DoesNotExist:
        return createError("Stream: "+ streamId +" does not exist")
        
    tweets = Tweet.objects.filter(stream=stream)
    
    results = { "name" : stream.name, "stream_id" : stream.stream_id, "categories" : { "politics" : 0, "sports" : 0, "science-technology" : 0, "food" : 0, "business" : 0, "healthy-living" : 0, "arts" : 0, "entertainment" : 0, "science" : 0, "other" : 0, "education" : 0, "religion" : 0, "none" : 0 }}
    
    for tweet in tweets:
        if tweet.category_confidence > float(categoryConfidence) and len(tweet.text) > 40 and tweet.text[0] != "@":
            results["categories"][tweet.category] = results["categories"][tweet.category] + 1 
            if tweet.category == "technology":
                log.debug(str(tweet.category_confidence) + " " +tweet.text + " " + str(categoryConfidence)) 
        else:
            results["categories"]["none"] = results["categories"]["none"] + 1
        
    response_data = { "success" : True, "results" : results }
    return HttpResponse(content=json.dumps(response_data), content_type="application/json")

def deleteStream(request):
    streamId = request.GET.get("stream_id","")
    
    try:
        stream = Stream.objects.get(stream_id=streamId)
        stream.delete()
    except Stream.DoesNotExist:
        return createError("Stream: "+ streamId +" does not exist")
    
    log.debug("deleting: " + stream.stream_id)
    
    response_data = { "success" : True }
    return HttpResponse(content=json.dumps(response_data), content_type="application/json")
    
def stopStream(request):
    streamId = request.GET.get("stream_id","")
    
    stream = None
    try:
        stream = Stream.objects.get(stream_id=streamId)
        stream.end_time = datetime.now()
        stream.save()
    except Stream.DoesNotExist:
        return createError("Stream: "+ streamId +" does not exist")
    
    dsUser = datasift.User(settings.DATASIFT["username"], settings.DATASIFT["api_key"])
    dsStream = dsUser.get_push_subscription(stream.stream_id)
    log.debug("stopping: " + stream.stream_id)
    
    # deleting datasift stream, not local stream object
    dsStream.delete()
        
    response_data = { "success" : True }
    return HttpResponse(content=json.dumps(response_data), content_type="application/json")

def getTweetsWithWord(request):
    
    streamId = request.GET.get("stream_id","")
    category = request.GET.get("category","")
    word = request.GET.get("word","")
    categoryConfidence = float(request.GET.get("category_confidence",0.0))
    
    stream = None
    try:
        stream = Stream.objects.get(stream_id=streamId)
    except Stream.DoesNotExist:
        return createError("Stream: "+ streamId +" does not exist")
    
    tweets = None
    
    if category!= "":
        tweets = Tweet.objects.filter(stream=stream, category=category, category_confidence__gt=float(categoryConfidence), text__icontains=word)
    else:
        tweets = Tweet.objects.filter(stream=stream, category_confidence__gt=float(categoryConfidence), text__icontains=word)
    
    results = []
    
    for tweet in tweets:
        
         if len(tweet.text) > 40 and tweet.text[0] != "@":
            results.append( { "text" : tweet.text, "category" : tweet.category, "confidence" : tweet.category_confidence })
        
    response_data = { "success" : True, "results" : results }
    log.debug(response_data)
    return HttpResponse(content=json.dumps(response_data), content_type="application/json")


def getStreamedTweets(request):
    
    streamId = request.GET.get("stream_id","")
    category = request.GET.get("category","")
    categoryConfidence = float(request.GET.get("category_confidence",0.0))
    
    stream = None
    try:
        stream = Stream.objects.get(stream_id=streamId)
    except Stream.DoesNotExist:
        return createError("Stream: "+ streamId +" does not exist")
    
    tweets = None
    
    if category!= "":
        tweets = Tweet.objects.filter(stream=stream, category=category, category_confidence__gt=float(categoryConfidence))
    else:
        tweets = Tweet.objects.filter(stream=stream, category_confidence__gt=float(categoryConfidence))
    
    results = []
    
    for tweet in tweets:
        
         if len(tweet.text) > 40 and tweet.text[0] != "@":
            results.append( { "text" : tweet.text, "category" : tweet.category, "confidence" : tweet.category_confidence })
        
    response_data = { "success" : True, "results" : results }
    #log.debug(response_data)
    return HttpResponse(content=json.dumps(response_data), content_type="application/json")

@csrf_exempt
def datasiftLog(request):
    
    data = json.loads(request.raw_post_data)
    
    if data != json.loads("{}"):        
        try:
            
            stream = Stream.objects.get(stream_id=data["id"])
            #log.debug("Got new batch of tweets for: " + stream.name);
            for interaction in data["interactions"]:
                if "deleted" in interaction.keys():
                    continue
                
                tweetText = u''.join(interaction["twitter"]["text"]).encode('utf-8')
                log.debug(tweetText)
                
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                
                knightCategories = requests.post("http://classify.knilab.com/classify/text/linear/",data="""input={text : '"""+tweetText+"""'}""",headers=headers).json()
                
                #log.debug(knightCategories)
                
                tweet = Tweet(stream=stream, text=tweetText, category=knightCategories[0][0], category_confidence=knightCategories[0][1], sentiment=interaction["salience"]["content"]["sentiment"] if "salience" in interaction.keys() else 0.0)
                tweet.save()
        except Stream.DoesNotExist:
            log.error("Received interactions for a stream that's not in the database! id: " + data["id"] + " hash: " + data["hash"])
            pass
        except Exception as e:
            log.error(e)
            log.error(data)
            pass
    
    #log.debug(data["interactions"][0]["twitter"]["text"])
    #log.debug(data)
    response_data = { "success" : True }
    return HttpResponse(content=json.dumps(response_data), content_type="application/json")

def datasiftStop(request):
    dsUser = datasift.User(settings.DATASIFT["username"], settings.DATASIFT["api_key"])
    subscriptions = dsUser.list_push_subscriptions()
    for subscription in subscriptions["subscriptions"]:
        s = dsUser.get_push_subscription(subscription.get_id())
        log.debug("deleting: " + str(subscription.get_id()))
        s.delete()
    
    response_data = { "success" : True }
    return HttpResponse(content=json.dumps(response_data), content_type="application/json")
    
def datasiftPushLog(request):
    dsUser = datasift.User(settings.DATASIFT["username"], settings.DATASIFT["api_key"])
    logs = dsUser.get_push_subscription_log()
    #log.debug(logs)
    return HttpResponse(content=json.dumps(logs), content_type="application/json")
    

def uploadImage(request):
    uploadImageForm = None
    if (request.method == "POST"):
        uploadImageForm = UploadImageForm(request.POST["stream_id"], request.POST, request.FILES)
        log.debug("uploadImage - method is post, errors: " + str(uploadImageForm.errors))
        log.debug("as_p(): " + uploadImageForm.as_p())
        
        if uploadImageForm.is_valid():
            log.debug("uploadImage - form is valid")
            cd = uploadImageForm.cleaned_data
            streamId = cd["stream_id"]
            image = cd["image"]
            
            stream = Stream.objects.get(stream_id=streamId)
            stream.image.save(stream.stream_hash, image)

    return dashboard(request)

@login_required(login_url='/ct/login/?next=/ct/dashboard/') 
def dashboard(request):
    trackForm = None
    if (request.method == "POST"):
        trackForm = TrackForm(request.POST)
        if trackForm.is_valid():
            
            cd = trackForm.cleaned_data
            twitterHandle = cd["twitter_handle"]
            timeToTrack = 0 #cd["time_to_track"]
            
            profile = Profile.objects.get(user=request.user)
            
            twitterObj = Twitter(auth=OAuth(profile.oauth_token, profile.oauth_secret, settings.TWITTER_KEY, settings.TWITTER_SECRET))
            twitterUser = twitterObj.users.show(screen_name=twitterHandle)
            
            trackedUsersString = ""
            count = 0
            
            try:
                listOfFollowersObj = twitterObj.followers.ids(screen_name=twitterHandle)
                
                while True:
                    listOfFollowers = listOfFollowersObj["ids"]            
                
                    for follower in listOfFollowers:
                        trackedUsersString += str(follower) + ","
                        
                    if listOfFollowersObj["next_cursor"] != 0 and count < 5: 
                        listOfFollowersObj = twitterObj.followers.ids(screen_name=twitterHandle,cursor=listOfFollowersObj["next_cursor"])
                        count = count + 1
                    else:
                        break
            except TwitterHTTPError as te:
                return createError("Twitter API Error: " + str(te)) 
            
            #log.debug(len(trackedUsersString))
            trackedUsersString = trackedUsersString[:-1] # get rid of last comma
            
            tu = None
            
            try:
                tu = TrackedUser.objects.get(twitter_id=twitterUser["id_str"])
                tu.track_until = datetime.now()+timedelta(minutes=int(timeToTrack))
                tu.followers_list = trackedUsersString
            except TrackedUser.DoesNotExist:
                tu = TrackedUser(twitter_id=twitterUser["id_str"], user=profile, track_until=datetime.now()+timedelta(minutes=int(timeToTrack)), followers_list=trackedUsersString, screen_name=twitterUser["name"])
                
            tu.save()
            
            dsUser = datasift.User(settings.DATASIFT["username"], settings.DATASIFT["api_key"])
            csdl = "return { language.tag == \"en\" and twitter.user.id in ["+trackedUsersString+"] }"
            #log.debug(csdl)
            
            streamDef = dsUser.create_definition(csdl)
            
            pushDef = dsUser.create_push_definition()
            pushDef.set_output_type("http")
            pushDef.set_output_param("delivery_frequency", 5)
            pushDef.set_output_param("max_size", 1000000)
            pushDef.set_output_param("format", "json")
            pushDef.set_output_param("url", "http://ec2-54-244-189-248.us-west-2.compute.amazonaws.com/ct/datasiftLog/")
            
            subscription = pushDef.subscribe_definition(streamDef, twitterHandle)
            
            sub = Stream(tracked_user=tu, stream_id=subscription.get_id(), stream_hash=subscription.get_hash(), name=subscription.get_name())
            sub.save()
            
            log.debug(subscription.get_status())
            log.error(sub.name + " id: " + sub.stream_id + " hash: " + sub.stream_hash)
            
    trackForm = TrackForm()
    
    results = []
    trackedUsers = TrackedUser.objects.filter(user=Profile.objects.get(user=request.user))
    
    for tu in trackedUsers:            
        streams = Stream.objects.filter(tracked_user=tu)
        for stream in streams:
            stream.count = len(Tweet.objects.filter(stream=stream))
            stream.uploadImageForm = UploadImageForm(stream.stream_id)
            results.append(stream)
            #log.debug(stream.name)
    
    return render(request, "track.html", {'track_form' : trackForm, "streams" : results, "twitter_handle" : request.session["screen_name"] })

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

    return HttpResponseRedirect('/ct/dashboard/')
