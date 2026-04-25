from django.contrib import admin
from .models import EventType, Event, EventSignup


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
    readonly_fields = ("created_on", "updated_on")

    list_display = (
        'title', 'category', 'organizer', 'description',
        'location', 'start_time', 'end_time',
        'created_on', 'updated_on',
    )

    list_filter = (
        'category', 'location', 'start_time',
        'end_time', 'created_on', 'updated_on',
    )

    fieldsets = [
        ('Details', {
            'fields': [
                'title',
                'category',
                'organizer',
                'event_image',
                'description',
                'location',
                ('start_time', 'end_time'),
                ('event_capacity', 'status'),
                ('created_on', 'updated_on'),
            ]
        }),
    ]


class EventSignupAdmin(admin.ModelAdmin):
    model = EventSignup
    search_fields = ('event',)
    list_display = ('event', 'user_registrant', 'new_registrant',)
    list_filter = ('event',)


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventSignup, EventSignupAdmin)