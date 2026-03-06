from django.db import models
from django.urls import reverse


# Must be sorted by name (ascending) .order_by(name)
class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


# Must be sorted by the date it was created (ascending) .order_by(created_on)
class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:detail_view', args=[int(self.id)])
