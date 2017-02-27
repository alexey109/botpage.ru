from django.contrib import admin

from .models import Rooms
from .models import Parameters
from .models import RoomsParameters
from .models import RoomsComments

class RoomsAdmin(admin.ModelAdmin):
	list_display = ('map_id', 'title', 'rtype')
	search_fields = ['map_id', 'title']
	list_filter = ['rtype']

admin.site.register(Rooms, RoomsAdmin)
admin.site.register(Parameters)
admin.site.register(RoomsParameters)
admin.site.register(RoomsComments)
