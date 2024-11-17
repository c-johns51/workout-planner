from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Routine(models.Model):
    """Represents a users workout routine."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="routines")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Exercise(models.Model):
    """"""
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name="exercises")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    primary_muscles = models.CharField(max_length=255, blank=True, null=True)
    images = models.URLField(blank=True, null=True)
    days = models.ManyToManyField('Day', related_name="exercises")

class Day(models.Model):
    """This model normalizes the data, making it easier to filter and group exercises by day."""
    name = models.CharField(max_length=10, unique=True)  # E.g., "Monday"