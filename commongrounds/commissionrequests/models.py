from django.db import models

# Must be sorted by name (ascending) .order_by(name)
class CommissionType(models.Models):
    name = models.CharField(max_length=255)
    description = models.TextField()

# Must be sorted by the date it was created (ascending) .order_by(created_on)
class Commission(models.Models):
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.IntegerField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
