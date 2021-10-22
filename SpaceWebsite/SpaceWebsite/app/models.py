"""
Definition of models.
"""

from django.db import models
import json

class Event (models.Model):
    title = models.CharField(max_length = 100)

    def __str__(self):
        return self.title

    def tojson(self):
        return json.dumps(self, default= lambda o: o.__dict__)


# Create your models here.
