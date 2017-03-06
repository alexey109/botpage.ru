#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from __future__ import unicode_literals
from django.db import models

class Groups(models.Model):
	gcode	= models.CharField(u'Номер группы', max_length=20, db_index=True)
	def __unicode__(self):
		return self.gcode 
	class Meta:
		managed = True
		verbose_name = u'группа'
		verbose_name_plural = u'группы'
		db_table = 'groups'

class Users(models.Model):
	vk_id			= models.CharField(u'ID в VK', max_length=50, blank=False, null=False, default='')
	vk_chat			= models.BooleanField(u'Тип диалога', default=False)
	my_id			= models.CharField(u'ID для бота', max_length=100, blank=False, null=False, default='')
	group			= models.ForeignKey(
						Groups, 
						on_delete=models.PROTECT, 
						verbose_name=u'Группа', 
						null=False, 
						default=''
					)
	notice_today	= models.BooleanField(u'Уведомление сегодня', default=False)
	notice_tommorow	= models.BooleanField(u'Уведомление завтра', default=False)
	notice_week		= models.BooleanField(u'Уведомление неделю', default=False)
	notice_map		= models.BooleanField(u'Уведомление где пара', default=False)
	
	def __unicode__(self):
		return self.my_id 
	
	class Meta:
		managed = True
		verbose_name = u'пользователь'
		verbose_name_plural = u'пользователи'
		db_table = 'users'
		index_together = [
			["vk_id", "vk_chat"],
		]
	
class Schedule(models.Model):
	group 	= models.ForeignKey(Groups, on_delete=models.CASCADE, verbose_name=u'Группа', db_index=True)
	week 	= models.CharField(u'Неделя', max_length=50, blank=True, null=True)
	day 	= models.SmallIntegerField(u'День')
	numb 	= models.SmallIntegerField(u'Номер')
	name 	= models.CharField(u'Название', max_length=100)
	room 	= models.CharField(u'Аудитория', max_length=20, blank=True, null=True)
	teacher	= models.CharField(u'Преподаватель', max_length=60, blank=True, null=True)
	
	def __unicode__(self):
		return self.name  
		
	class Meta:
		managed = True
		verbose_name = u'расписание'
		verbose_name_plural = u'расписания'
		db_table = 'schedule'
		

class UsersSchedule(models.Model):
	user 	= models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name=u'Пользователь', db_index=True)
	name 	= models.CharField(u'Название', max_length=100, blank=False, null=False, default='')
	day 	= models.SmallIntegerField(u'День', null=False, default=0)
	numb 	= models.SmallIntegerField(u'Номер', null=False, default=0)
	teacher	= models.CharField(u'Преподаватель', max_length=60, blank=True, null=True)
	week 	= models.CharField(u'Неделя', max_length=50, blank=True, null=True)
	room 	= models.CharField(u'Аудитория', max_length=20, blank=True, null=True)
	hide	= models.BooleanField(u'Пустая пара', default=False)
	
	def __unicode__(self):
		return self.name  
		
	class Meta:
		managed = True
		verbose_name = u'расписание пользователей'
		verbose_name_plural = u'расписания пользователей'
		db_table = 'users_schedule'
		

	
