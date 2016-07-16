from .forms import Userform
from django.shortcuts import render
from django.http import Http404,HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate ,login,logout
from .models import *
from django.views import generic
from django.http.response import HttpResponse
import json, random ,re, requests,urllib,urllib.request
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist

def home(request):
	import simplejson, urllib
	orig_lat, orig_lng=10,10
	dest_lat, dest_lng=20,20
	orig_coord = orig_lat, orig_lng
	dest_coord = dest_lat, dest_lng
	url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
	#result= simplejson.load(urllib.urlopen(url))
	result = requests.get(url).json()
	#driving_time = result['rows'][0]['elements'][0]['duration']['value']
	return HttpResponse(result)


def register(request):
	if request.method=='POST':
		form=Userform(request.POST)
		if form.is_valid():
			user=form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			user2=authenticate(username=username,password=password)
			if user2 is not None:
				login(request,user2)
				return HttpResponseRedirect('/index/')
		return render(request,'registration.html',{'form':form})
	else:
		form=Userform(None)
		return render(request,'registration.html',{'form':form})

def logintoit(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			return HttpResponseRedirect('/index/')
		return render(request,'login.html',{})

	else:
		return render(request,'login.html',{})

def logout1(request):
	logout(request)
	return HttpResponseRedirect('/account/login/')
	
def index(request):
	if request.user.is_authenticated():
		user=request.user
		if request.method=="GET":
			try :
				obj=Userform.objects.get(user=user)
				return HttpResponseRedirect('/')
			except ObjectDoesNotExist:
				return render(request,'index.html',{})
		else:
			temp=request.POST.get('flag')
			if flag=='ware':
				sam=Userform.objects.create(user=user,flag=1)
				sam.save()
			else:
				sam=Userform.objects.create(user=user,flag=2)
				sam.save()
			return HttpResponseRedirect('/')


