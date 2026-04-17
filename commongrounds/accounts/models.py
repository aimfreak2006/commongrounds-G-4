from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    display_name = models.CharField(max_length=63)
    email = models.EmailField()
    role = models.CharField(
        choices=[
            ('Normal User', 'Normal User'),
            ('Market Seller', 'Market Seller'),
            ('Event Organizer', 'Event Organizer'),
            ('Book Contributor', 'Book Contributor'),
            ('Project Creator', 'Project Creator'),
            ('Commission Maker', 'Commission Maker'),
        ],
        default='Normal User'
    )

    def __str__(self):
        return f"{self.display_name}"
