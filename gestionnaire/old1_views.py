from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django import template
from django.conf import settings

def index(request):
    return HttpResponse("Hello Django") 

def today_is(request):
    now = datetime.datetime.now()
    return render(request,'gestionnaire/datetime.html', {
			'now': now, 
			'template_name':'gestionnaire/nav.html',
			'base_dir':settings.BASE_DIR }
		)


