# _*_ coding:utf-8 _*_
# Create your views here.
from django.template import Template, Context
from django.shortcuts import render_to_response
from srvMonitor.models import *

from django.contrib.auth.decorators import login_required  
from django.contrib import auth

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

import datetime 
from urllib2 import Request

def index(request):
	# current_date=datetime.datetime.now()
	if request.user.is_authenticated():
		'if the session remains , auto login'
		return render_to_response('srvMonitor/srvstatus.html')
	else:
		return render_to_response('login.html')
	

@login_required
def srvlist(request):
	srvlist=srvInfo.objects.all()
	return render_to_response('srvMonitor/srvlist.html',{'srvlist':srvlist})
 	
@login_required
def tmpstatus(request):
	tmpstatus=tmpStatus.objects.all()
	return render_to_response('srvMonitor/tmpstatus.html',{'tmpstatus':tmpstatus})

@login_required	
def srvstatus(request):
	# srvstatus=srvStatus.objects.filter(alert_level='4')
	srvstatus=srvStatus.objects.all().order_by('-ts')[0:9]
# 	print "sessionid",request.session.get('session_id')

	return render_to_response('srvMonitor/srvstatus.html',{'srvstatus':srvstatus})
	
def login(request):
# 	username=request.POST.get('username')
# 	password=request.POST.get('password')
	username=request.GET.get('username')
	password=request.GET.get('password')
# 	print username
# 	print password
	User=auth.authenticate(username=username,password=password)
	
	if User is not None and User.is_active:
		auth.login(request,User)
		return render_to_response('srvMonitor/srvstatus.html')
	else:
		return render_to_response('login.html',{'error':"用户名密码错误"})
	
def logout(request):
	auth.logout(request)
	return render_to_response('login.html')
	
def test(request):
	student_dict=['12','23','34','34','34']
	cities = [
    {'name': 'Mumbai', 'population': '19,000,000', 'country': 'India'},
    {'name': 'Calcutta', 'population': '15,000,000', 'country': 'India'},
    {'name': 'New York', 'population': '20,000,000', 'country': 'USA'},
    {'name': 'Chicago', 'population': '7,000,000', 'country': 'USA'},
    {'name': 'Tokyo', 'population': '33,000,000', 'country': 'Japan'},
]
# 	student_dict=[]
	return render_to_response('srvMonitor/test.html',{"cities":cities})