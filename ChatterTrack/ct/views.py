# Create your views here.
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
import json


def createError(msg):
  response_data = { "error" : -1, "message" : msg }
  return HttpResponseBadRequest(content=json.dumps(response_data), content_type="application/json")
  
  
def index(request):
  response_data = { "error" : -1, "message" : "test" }
  return HttpResponse(content=json.dumps(response_data), content_type="application/json")
