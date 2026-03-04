from django.contrib import admin
from .models import EventType, Event

class EventInLIne(admin.TabularInline):
    model = Event

class EventTypeAdmin(admin.ModelAdmin):
    model = EventType
    search_fields = ('name',)
    list_display = ('name', 'description',)
    inline = [EventInLIne,]

class EventAdmin(admin.ModelAdmin):
    model = EventType
    search_fields = ('title', 'category',)

    list_display = (
        'title', 'category', 'description',
        'location', 'start_time', 'end_time',
        'created_on', 'updated_on',
        )
    
    list_filter = (
        'description', 'location', 'start_time',
        'end_time', 'created_on', 'updated_on',
        )
    
    fieldsets = [
        ('Details', {
            'fields':[
                ('title', 'description', 'location',
                 'start_time', 'end_time', 'created_on',
                 'updated_on',),
                'category',
            ]
        }),
    ]

admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
