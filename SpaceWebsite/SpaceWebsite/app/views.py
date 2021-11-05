"""
Definition of views.
"""

from datetime import datetime

from django.core import serializers
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Event


def event_list(request, **kwargs):
    """Return JSON for all events with search and sorting"""
    events = Event.objects.all()
    title = request.GET.get('title')
    sort_up = request.GET.get('sort_up')
    sort_down = request.GET.get('sort_down')
    date = request.GET.get('date')
    text = request.GET.get('text')

    if title is not None:
        events = events.filter(title__iexact=title)
    if date is not None:
        events = events.filter(begin_date__iexact=date)
    if text is not None:
        events = events.filter(description__contains=text)
    if sort_up:
        events = events.order_by('-begin_date')
    if sort_down:
        events = events.order_by('begin_date')

    return HttpResponse([x.tojson() for x in list(events)])


def event_list_id(request, event_id):
    """Return JSON for event by id"""
    e = Event.objects.get(pk=event_id)
    return HttpResponse(e.tojson())


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )
