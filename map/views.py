from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Rooms

def index(request):
	template = loader.get_template('map/index.html')
	all_rooms = Rooms.objects.all()
	context = {
		'all_rooms': all_rooms,
	}
	return HttpResponse(template.render(context, request))

