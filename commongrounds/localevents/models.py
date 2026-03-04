from django.db import models
from django.urls import reverse

class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return '{}'.format(self.name)
    
    class Meta:
        ordering = ['name',]
        unique_together = ['name', 'description',]
        verbose_name = 'event_type'
        verbose_name_plural = 'event_types'

class Event(models.Model):
    title = models.CharField(max_length=255)
    
    category = models.ForeignKey(
        EventType,
        on_delete=models.CASCADE,
        related_name='events'
    )

    description = models.TextField()

    location = models.CharField()

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    created_on = models.DateTimeField()

    updated_on = models.DateTimeField()

    def __str__(self):
        return '{} last update on {}'.format(self.title, self.updated_on)
    
    def get_absolute_url(self):
        return reverse('localevents:event_detail', args=[str(self.pk)])
    
    class Meta:
        ordering = ['start_time',]
        unique_together = ['title', 'created_on',]
        verbose_name = 'event'
        verbose_name_plural = 'events'