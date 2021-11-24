"""
Definition of models.
"""

import datetime
import json

from django.db import models
from djrichtextfield.models import RichTextField
from django.conf.urls.static import static
from django.conf import settings
from embed_video.fields  import  EmbedVideoField


def _event_json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    if isinstance(value, datetime.time):
        return dict(hour=value.hour, minute=value.minute, second=value.second)
    else:
        return value.__dict__


class News(models.Model):
    title = models.CharField(max_length = 100, verbose_name = 'Заголовок')
    text = RichTextField(verbose_name='Текст')
    publishing_date = models.DateTimeField(verbose_name = 'Дата публикации')
    picture = models.ImageField(null=True, blank=True)
    video = EmbedVideoField(null=True, blank=True)
    
    def __str__(self):
        return self.title 
    class Meta:
        verbose_name = u"Новость"
        verbose_name_plural = u"Новости"

class CommonText(models.Model):
    title = models.CharField(max_length = 100, verbose_name = 'Название')
    text = RichTextField(verbose_name='Текст')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = u"Текст для раздела"
        verbose_name_plural = u"Тексты для разделов"

class EventCategory(models.Model):
    type = models.CharField(max_length=100, null=True, verbose_name= 'Название')
    class Meta:
        verbose_name = u"Тип события"
        verbose_name_plural = u"Типы событий"
    def __str__(self):
        return self.type


class Event(models.Model):
    class Meta:
        verbose_name = u"Событие"
        verbose_name_plural = u"События"

    title = models.CharField(max_length=100, blank=False, verbose_name='Название')
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, null=True, blank=False, verbose_name='Тип')
    description = models.TextField(blank=False, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='events_images', height_field=None, width_field=None,
                              max_length=100, blank=True, null=True,verbose_name='Иллюстрация')
    begin_date = models.DateField(blank=True, null=True, verbose_name='Дата начала')
    end_data = models.DateField(blank=True, null=True, verbose_name='Дата окончания')
    begin_time = models.TimeField(blank=True, null=True, verbose_name='Время начала')
    end_time = models.TimeField(blank=True, null=True, verbose_name='Время окончания')

    def __str__(self):
        return self.title

    def tojson(self):
        return json.dumps(self, default=_event_json_default).encode('utf-8')
