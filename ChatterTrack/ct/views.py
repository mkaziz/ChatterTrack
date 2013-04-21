# Create your views here.
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
import json, requests, twitter


def createError(msg):
    response_data = { "error" : -1, "message" : msg }
    return HttpResponseBadRequest(content=json.dumps(response_data), content_type="application/json")
  
  
def index(request):
    response_data = { "error" : -1, "message" : "test" }
    return render(request, "index.html")
  #return HttpResponse(content=json.dumps(response_data), content_type="application/json")

def twitter_login(request):
    
    consumerKey = "b4G5PKMYYFsFLIrrTsbA"
    consumerSecret = "pSM2rv4TJDnC1pJKIZeU7W2mR3E3mOOuluZhnyn4"
    
    baseUrl = "https://api.twitter.com/"
    method = "oauth/request_token"
    params = {"oauth_callback" : twitter.oauth.urlencode_noplus("twitter")}
    
    #auth=OAuth(oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET)
    auth = OAuth("", "", consumerKey, consumerSecret)
    
    auth.encode_params(baseUrl, method, params)
    
    return createError("it works!")
