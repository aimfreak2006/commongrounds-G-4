from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Commission(models.Model):
    class Status(models.TextChoices):
        OPEN = '0O', _("Open")
        FULL = '1F', _("Full")
        COMPLETED = '2C', _("Completed")
        DISCONTINUED = '3D', _("Discontinued")

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.ForeignKey(
        CommissionType,
        on_delete=models.CASCADE,
        related_name='commissions',
        null=True
    )
    people_required = models.IntegerField()
    status = models.CharField(
        choices=Status,
        default=Status.OPEN
    )
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['status','created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:detail_view', args=[int(self.id)])
    

class Job(models.Model):
    class Status(models.TextChoices):
        OPEN = 'O', _("Open")
        CLOSE = 'F', _("Full")

    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        null=True
    )
    role = models.CharField(max_length=255)
    manpower_required = models.IntegerField()
    status = models.CharField(
        max_length=255,
        choices=Status,
        default=Status.OPEN
    )

    class Meta:
        ordering = ['-status', '-manpower_required', 'role']


class JobApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = '0P', _("Pending")
        ACCEPTED = '1A', _("Accepted")
        REJECTED = '2R', _("Rejected")

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=True
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=255,
        choices=Status,
        default=Status.PENDING
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['status', "-applied_on"]
