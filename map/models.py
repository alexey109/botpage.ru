#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from django.db import models


class Rooms(models.Model):
	map_id	= models.CharField(u'ID на карте', max_length=20, blank=True, null=True)
	title	= models.CharField(u'Название', max_length=30, blank=True, null=True)
	rtype	= models.SmallIntegerField(u'Тип аудитории', blank=True, null=True, default=0) 
		
	def __unicode__(self):
		return self.map_id  
		
	class Meta:
		managed = True
		verbose_name = u'аудитория'
		verbose_name_plural = u'аудитории'
		db_table = 'rooms'
	
class Parameters(models.Model):
	pname	= models.CharField(u'Название', max_length=50)
	ptype	= models.IntegerField(u'Тип данных') 
		
	def __unicode__(self):
		return self.pname  
		
	class Meta:
		managed = True
		verbose_name = u'вид параметра'
		verbose_name_plural = u'виды параметров'
		db_table = 'parameters'
	
class RoomsParameters(models.Model):
	room 	= models.ForeignKey(Rooms, on_delete=models.CASCADE, verbose_name=u'Аудитория')
	param 	= models.ForeignKey(Parameters, on_delete=models.CASCADE, verbose_name=u'Параметры')
	int_val	= models.IntegerField(u'Значение integer', blank=True, null=True) 
	flo_val	= models.FloatField(u'Значение float', blank=True, null=True)
	str_val	= models.CharField(u'Значение string', max_length=200, blank=True, null=True)
	dat_val	= models.DateTimeField(u'Значение datetime', blank=True, null=True)
    
	def __unicode__(self):
		return self.room + self.param  
		
	class Meta:
		managed = True
		verbose_name = u'параметр аудитории'
		verbose_name_plural = u'параметры аудиторий'
		db_table = 'rooms_parameters'
	
class RoomsComments(models.Model):
	room 	= models.ForeignKey(Rooms, on_delete=models.CASCADE, verbose_name=u'Аудитория')
	comment	= models.CharField(u'Комментарий', max_length=50, blank=True, null=True)
	visible	= models.BooleanField(u'Виден пользователям', default=False)
	add_date= models.DateTimeField(u'Дата добавления', auto_now_add=True)
    	
	def __unicode__(self):
		return self.comment  
		
	class Meta:
		managed = True
		verbose_name = u'комментарий к аудиториям'
		verbose_name_plural = u'комментарии к аудиториям'
		db_table = 'rooms_comments'
	
