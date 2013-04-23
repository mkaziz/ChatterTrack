# Django imports
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# python imports
import json, requests, twitter, urlparse
from urllib import quote
import oauth2 as oauth
import cgi

def createError(msg):
    response_data = { "error" : -1, "message" : msg }
    return HttpResponseBadRequest(content=json.dumps(response_data), content_type="application/json")
  
@login_required(login_url='/ct/login/') 
def index(request):
    response_data = { "error" : -1, "message" : "test" }
    return render(request, "index.html")
  #return HttpResponse(content=json.dumps(response_data), content_type="application/json")

def login(request):
    return render(request, "login.html")

def twitter_login(request):
    
    baseUrl = "https://api.twitter.com/"
    method = "oauth/request_token"
    params = { "oauth_callback" : "http://ec2-54-244-189-248.us-west-2.compute.amazonaws.com/ct/twitter_login_handler/" }
    
    return createError()

