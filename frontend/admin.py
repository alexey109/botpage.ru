from django.contrib import admin

from .models import Schedule
from .models import UsersSchedule
from .models import Groups
from .models import Users


class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'group_id', 'week', 'day', 'numb', 'name', 'room', 'teacher')
    search_fields = ['group_id', 'teacher']
    list_filter = ['group_id']


class GroupsAdmin(admin.ModelAdmin):
    search_fields = ['gcode']


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'vk_id',
        'is_chat',
        'group',
        'notice_today',
        'notice_tommorow',
        'notice_week',
        'notice_map',
        'send_time',
        'notice_zerohour',
        'bot_activity'
    )
    search_fields = ['vk_id', 'bot_id']


class UsersScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'name', 'teacher', 'week', 'day', 'numb', 'room',
        'hide')
    search_fields = ['name', 'user']
    list_filter = ['user']


admin.site.register(Groups, GroupsAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(UsersSchedule, UsersScheduleAdmin)
