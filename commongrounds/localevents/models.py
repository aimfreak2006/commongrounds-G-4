from django.db import models
from datetime import datetime
from django.urls import reverse

# Create your models here.
class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return '{}'.format(self.name)

class Event(models.Model):
    title = models.CharField(max_length=255)
    
    category = models.ForeignKey(
        EventType,
        on_delete=models.CASCADE
    )

    description = models.TextField()

    location = models.CharField()

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    created_on = models.DateTimeField(auto_now_add=True)

    updated_on = models.DateTimeField(auto_now=True)