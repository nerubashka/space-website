"""
Definition of models.
"""

import json

from django.db import models


class EventCategory(models.Model):
    type = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.type


class Event(models.Model):
    title = models.CharField(max_length=100, blank=False)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, null=True, blank=False)
    description = models.TextField(blank=False, null=True)
    image = models.ImageField(upload_to='events_images', height_field=None, width_field=None,
                              max_length=100, blank=True, null=True)
    begin_date = models.DateField(blank=True, null=True)
    end_data = models.DateField(blank=True, null=True)
    begin_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def tojson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
