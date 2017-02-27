#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime as dt
import re
import hashlib
import time


from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Schedule
from .models import Users
from .models import Groups
from .models import UsersSchedule


def adjustText(text, max_len = 23):
	if len(text) < max_len:
		return text
	end_len 	= -3
	adjusted 	= ''
	start	= text[:(max_len + end_len - 2)] + '..'
	end		= text[end_len:]
	
	return start + end
	
def isThatWeek(native_week, base_week):
	if native_week == '':
		result = True
	elif 'I' in native_week:
		result = (base_week % 2 == 0) == (native_week.strip() == 'II')
	elif '-' in native_week:
		period = re.split('-', native_week)
		result = (base_week >= int(period[0])) and (base_week <= int(period[1]))
	else:
		result = str(base_week) in re.split(r'[\s,]', native_week)
	return result

def getWeekRange(week_numb):
	week_numb = week_numb + dt.date(2017, 2, 6).isocalendar()[1] - 1
	date = dt.datetime.strptime("2017-{}-0".format(week_numb), "%Y-%W-%w")
	start = (date - dt.timedelta(days=6)).strftime('%d.%m')
	end = date.strftime('%d.%m')
	return "{} - {}".format(start, end)


def promo(request):
	msg = ''
	user_group = ''
	user_id = ''
	
	auth = request.POST.get('auth', '')
	
	if '-' in auth:
		user_group = auth.lower()
	else:
		user_id = auth
		
	if user_group:
		try:
			group = Groups.objects.get(gcode = user_group)
			request.session['group'] = group.gcode.upper()
			request.session['group_id'] = group.id	
			msg = u'Вы вошли! Группа ' + group.gcode.upper()
		except:
			msg = u'Ошибка, группа не найдена!'
	elif user_id:
		try:
			user = Users.objects.get(my_id = user_id)
			group = user.group
			request.session['user_id'] = user.id
			request.session['group_id'] = group.id
			request.session['group'] = group.gcode.upper()		
			msg = u'Вы вошли! Группа ' + group.gcode.upper()
		except Exception as e:
			msg = u'Ошибка, неверный ID!'
	
	context = {
		'msg' 		: msg,
		'group' 	: request.session.get('group', ''),
		'user_id'	: request.session.get('user_id', '')
	}
	template = loader.get_template('frontend/promo.html')
	return HttpResponse(template.render(context, request))

def editor(request):
	# prepare permanent data
	first 		= 1 # fisrt lesson number
	last		= 7 # last lesson number
	time_delay	= 3 # seconds
	hash_append	= 'd51a18a32b' # some string to make hash unpredictable
	lection_time = {
		1: ['I',	'9:00 10:30'],
		2: ['II',	'10:40 12:10'],
		3: ['III',	'13:00 14:30'],
		4: ['IV',	'14:40 16:10'],
		5: ['V',	'16:20 17:50'],
		6: ['VI',	'18:00 19:30'],
	}
	
	# Get user object
	wrong_user = False
	user_notice = {}
	try:
		session_user = Users.objects.get(id = request.session.get('user_id', ''))
		user_notice = {
			'today'		: session_user.notice_today,
			'tomorrow'	: session_user.notice_tommorow,
			'week'		: session_user.notice_week,
			'map'		: session_user.notice_map
		}
	except:
		wrong_user = True
		
	# form block
	# |
	# V
	input_name = request.POST.get('name', '')
	if not wrong_user and input_name and (time.time()-request.session.get('db_access_time', 0)> time_delay):
		
		request.session['db_access_time'] = time.time()
		request.session['mode_base'] = False
		try:
			rec_id = request.POST.get('rec_id', '')
			if rec_id[-1] == '1':
				raise Exception('Not user event!')
				
			# Check hashes for equal
			if str(hash(rec_id + hash_append)) == request.POST.get('id_hash', ''):
				# update UsersSchedule record
				user_event = UsersSchedule.objects.get(id = int(rec_id[:-1]))
				if bool(request.POST.get('delete', False)):
					user_event.delete()
				else:
					user_event.name		= input_name
					user_event.teacher	= request.POST.get('teacher', '')
					user_event.week		= request.POST.get('week', '')
					user_event.room		= request.POST.get('room', '')
					user_event.hide		= False
					user_event.save()
		except:
			user_event = UsersSchedule(
				user	= session_user,
				name	= input_name,
				day		= int(request.POST.get('day', 0)),
				numb	= int(request.POST.get('numb', 0)),
				teacher	= request.POST.get('teacher', ''),
				week	= request.POST.get('week', ''),
				room	= request.POST.get('room', ''),
				hide	= bool(request.POST.get('hide', False)),
			)
			user_event.save()
	
	# schedule block
	# |
	# V
	# generate empty schedule table with "event number - event day" element
	event_rows = {}
	for lnumb in range(first, last):
		event_rows[lnumb] = {}
		for day in range(0,6):
			event_rows[lnumb][day] = []
	# get data and put it in prepared table
	schedule_basic = Schedule.objects.filter(group = request.session.get('group_id', '-1'))	
	if request.session.get('mode_base', True):
		schedule_user = []
	else:
		schedule_user = UsersSchedule.objects.filter(user = request.session.get('user_id', '-1'))
	schedule_full = []
	# prepare basic schedule for html page
	for event_basic in schedule_basic:
		no_major = True
		hide = False
		for event_user in schedule_user:
			if event_basic.day == event_user.day \
			and event_basic.numb == event_user.numb \
			and event_basic.week == event_user.week:
				no_major = False
				if event_user.hide:
					hide = True
				break
		if no_major:
			my_id = str(event_basic.id) + '1'	# id start with 1 -> basic schedule table
			event = {
				'id'		: my_id,
				'id_hash'	: hash(my_id + hash_append),
				'name'		: event_basic.name,
				'day'		: event_basic.day,
				'numb'		: event_basic.numb,
				'teacher'	: event_basic.teacher,
				'week'		: event_basic.week,
				'room'		: event_basic.room,
				'hide'		: hide,
				'is_user'	: False
			}
			schedule_full.append(event)	
	# add user schedule for html page
	for event_user in schedule_user:
		my_id = str(event_user.id) + '0'	# id start with 1 -> basic schedule table
		event = {
			'id'		: my_id,
			'id_hash'	: hash(my_id + hash_append),
			'name'		: event_user.name,
			'day'		: event_user.day,
			'numb'		: event_user.numb,
			'teacher'	: event_user.teacher,
			'week'		: event_user.week,
			'room'		: event_user.room,
			'hide'		: event_user.hide,
			'is_user'	: True
		}
		schedule_full.append(event)		
	
	# convert data for schedule table
	for event in schedule_full:
		week = event['week'] + u' н.' if event['week'] else '-' 
		room = event['room'] if event['room'] else '-' 
		teacher = event['teacher'] if event['teacher'] else '-'
		event_rows[event['numb']][event['day']].append({
			'id'		: event['id'],
			'name'		: adjustText(event['name']),
			'room'		: room,
			'teacher'	: adjustText(teacher),
			'week'		: adjustText(week, 14),
			'hide'		: event['hide'],
			'is_user'	: event['is_user']
		})
	
		
	# combine prepared data with loaded schedule
	table_content = {}
	for lnumb in range(first, last):
		table_content[lnumb] = {
			'liter'	: lection_time[lnumb][0],
			'time'	: lection_time[lnumb][1],
			'events': event_rows[lnumb]
		}
	
	# set base/user mode
	mode = {
		'base' : request.session.get('mode_base', True),
		'user' : not request.session.get('mode_base', True),
	}
	view = {
		'teacher'	: request.session.get('view_teacher', False), 
		'weekroom'	: request.session.get('view_weekroom', True)
	}
	context = {
		'schedule_full'	: schedule_full,
		'table_content'	: table_content,
		'group' 		: request.session.get('group', ''),
		'mode'			: mode, 
		'view'			: view,
		'user_notice'	: user_notice,
	}
	template = loader.get_template('frontend/editor.html')
	return HttpResponse(template.render(context, request))

def schedule(request, page_week):
	# prepare permanent data
	if not page_week or int(page_week) > 16 or int(page_week) < 1:
		dat = dt.datetime.now()
		page_week = dt.datetime.now().isocalendar()[1] - dt.date(2017, 2, 6).isocalendar()[1] + 1
	page_week = int(page_week)
	first 	= 1 # fisrt lesson number
	last	= 7 # last lesson number
	lection_time = {
		1: ['I',	'9:00 10:30'],
		2: ['II',	'10:40 12:10'],
		3: ['III',	'13:00 14:30'],
		4: ['IV',	'14:40 16:10'],
		5: ['V',	'16:20 17:50'],
		6: ['VI',	'18:00 19:30'],
	}

	# generate week numbers for week panel at top of page
	week_panel = {}
	for i in range(1, 17):
		week_panel[i] = {
			'status'	: i == page_week,
			'range'		: getWeekRange(i),
		}
	# generate empty schedule table with "event number - event day" element
	event_rows = {}
	for lnumb in range(first, last):
		event_rows[lnumb] = {}
		for day in range(0,6):
			event_rows[lnumb][day] = []
	# get data and put it in prepared table
	schedule_basic = Schedule.objects.filter(group = request.session.get('group_id', '-1'))	
	schedule_user = UsersSchedule.objects.filter(user = request.session.get('user_id', '-1'))
	schedule_full = []
		
	for event_basic in schedule_basic:
		if not isThatWeek(event_basic.week, page_week):
			continue
		no_major = True
		for event_user in schedule_user:
			if event_basic.day == event_user.day \
			and event_basic.numb == event_user.numb \
			and event_basic.week == event_user.week:
				no_major = False
				break
		if not no_major:
			continue
		event = {
			'name'		: event_basic.name,
			'day'		: event_basic.day,
			'numb'		: event_basic.numb,
			'teacher'	: event_basic.teacher,
			'week'		: event_basic.week,
			'room'		: event_basic.room,
			'hide'		: False,
			'is_user'	: False
		}
		schedule_full.append(event)	
	for event_user in schedule_user:
		if not isThatWeek(event_user.week, page_week) or event_user.hide:
			continue			
		event = {
			'name'		: event_user.name,
			'day'		: event_user.day,
			'numb'		: event_user.numb,
			'teacher'	: event_user.teacher,
			'week'		: event_user.week,
			'room'		: event_user.room,
			'hide'		: event_user.hide,
			'is_user'	: True
		}
		schedule_full.append(event)
			
	for event in schedule_full:
		week = event['week'] + u' н.' if event['week'] else '-' 
		room = event['room'] if event['room'] else '-' 
		event_rows[event['numb']][event['day']].append({
			'name'	: adjustText(event['name']),
			'room'	: room,
			'teacher': event['teacher'],
			'week'	: adjustText(week, 14),
		})
		
	# combine prepared data with loaded schedule for template
	table_content = {}
	for lnumb in range(first, last):
		table_content[lnumb] = {
			'liter'	: lection_time[lnumb][0],
			'time'	: lection_time[lnumb][1],
			'events': event_rows[lnumb]
		}
	context = {
		'week_panel'	: week_panel,
		'table_content'	: table_content,
		'group' 		: request.session.get('group', ''),
	}
	template = loader.get_template('frontend/schedule.html')
	return HttpResponse(template.render(context, request))

def map(request):
	template = loader.get_template('map/index.html')
	return HttpResponse(template.render(request))

def help(request):
	template = loader.get_template('frontend/help.html')
	return HttpResponse(template.render( request))

def switcher(request, switcher_id):
	try:
		if switcher_id in ['mode_base', 'mode_user']:
			if request.session.get('user_id', False):
				request.session['mode_base'] = not request.session.get('mode_base', True)
			
		elif switcher_id == 'view_teacher':
			request.session['view_teacher'] = not request.session.get('view_teacher', False)
			
		elif  switcher_id == 'view_weekroom':
			request.session['view_weekroom'] = not request.session.get('view_weekroom', False)

		elif switcher_id in ['notice_today', 'notice_tomorrow', 'notice_week', 'notice_map']:
			session_user = Users.objects.get(id = request.session.get('user_id', ''))
			if switcher_id == 'notice_today':
				session_user.notice_today = not session_user.notice_today
			elif switcher_id == 'notice_tomorrow':
				session_user.notice_tommorow = not session_user.notice_tommorow
			elif switcher_id == 'notice_week':
				session_user.notice_week = not session_user.notice_week
			elif switcher_id == 'notice_map':
				session_user.notice_map = not session_user.notice_map
			session_user.save()
	except Exception as e:
		return HttpResponse(str(e))
	return HttpResponse(switcher_id)	
	
	
