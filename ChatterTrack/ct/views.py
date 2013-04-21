# Create your views here.
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
import json, requests, twitter, urlparse
from urllib import quote

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
    params = { "oauth_callback" : "http://ec2-54-244-189-248.us-west-2.compute.amazonaws.com/ct/twitter_login_handler/" }
    
    #auth=OAuth(oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET)
    auth = twitter.OAuth("", "", consumerKey, consumerSecret)
    oauth_token, oauth_token_secret = parse_oauth_tokens(
        twitter.oauth.request_token())
    
    encodedParams = dict(urlparse.parse_qsl(auth.encode_params(baseUrl, method, params)))
    
    headers={ "Authorization" : \
    "OAuth oauth_callback=\"" + encodeWord(encodedParams["oauth_callback"]) + "\"," + \
    "oauth_consumer_key=\"" + encodeWord(encodedParams["oauth_consumer_key"]) + "\"," + \
    "oauth_nonce=\"" + encodeWord(encodedParams["oauth_nonce"]) + "\"," + \
    "oauth_signature=\"" + encodeWord(encodedParams["oauth_signature"]) + "\"," + \
    "oauth_signature_method=\"" + encodeWord(encodedParams["oauth_signature_method"]) + "\"," + \
    "oauth_timestamp=\"" + encodeWord(encodedParams["oauth_timestamp"]) + "\"," + \
    "oauth_version=\"" + encodeWord(encodedParams["oauth_version"]) + "\"" }
    
    response = requests.post(baseUrl+method, headers=headers.items())
    r = response.request.headers
    t = response.text
    
    return createError()

def encodeWord(w):
    if type(w) is unicode: w = w.encode('utf-8')
    w = quote(w,safe='').replace("+", "%20")
    return w
    
def encodeHeaders(query):
    
    headers = {}
    for k,v in query:
        if type(k) is unicode: k = k.encode('utf-8')
        if type(v) is unicode: v = v.encode('utf-8')
        v = quote(v,safe='').replace("+", "%20")
        headers[k] = v
        
    return headers


def twitter_login_handler(request):
    
    
    return createError("reached twitter login handler")


def parse_oauth_tokens(result):
    for r in result.split('&'):
        k, v = r.split('=')
        if k == 'oauth_token':
            oauth_token = v
        elif k == 'oauth_token_secret':
            oauth_token_secret = v
    return oauth_token, oauth_token_secret
