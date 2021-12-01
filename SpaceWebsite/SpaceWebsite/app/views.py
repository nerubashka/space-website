"""
Definition of views.
"""
# -*- coding: utf-8 -*-


from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.core import serializers
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import Event, News, CommonText

def get_event_list(request, **kwargs):
    events = Event.objects.all()
    title = request.GET.get('title')
    sort_up = request.GET.get('sort_up')
    sort_down = request.GET.get('sort_down')
    date = request.GET.get('date')
    text = request.GET.get('text')
    uptodate = request.GET.get('uptodate')

    if title is not None:
        events = events.filter(title__iexact=title)
    if date is not None:
        events = events.filter(begin_date__iexact=date)
    if uptodate:
        events = events.filter(end_data__gte = datetime.now())
    if text is not None:
        events = events.filter(description__contains=text)
    if sort_up:
        events = events.order_by('-begin_date')
    if sort_down:
        events = events.order_by('begin_date')

    return events

def event_list(request, **kwargs):
    """Return JSON for all events with search and sorting"""
    events = get_event_list(request, **kwargs)
    return HttpResponse([x.tojson() for x in list(events)])

def event_list_id(request, event_id):
    """Return JSON for event by id"""
    e = Event.objects.get(pk=event_id)
    return HttpResponse(e.tojson())



class EventListView(ListView):
    model = Event
    template_name = 'app/events.html'
    page_name = 'events'
    news = News.objects.all().order_by('-publishing_date')[:5]
    paginate_by = 5
    ordering = ['begin_date']
    event_from_filter = datetime.today()
    

    def get_queryset(self):
        events = Event.objects.all().order_by('begin_date')
        title = self.request.GET.get('title')
        sort_up = self.request.GET.get('sort_up')
        sort_down = self.request.GET.get('sort_down')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        text = self.request.GET.get('text')
        uptodate = self.request.GET.get('uptodate')

        if title:
            events = events.filter(title__icontains=title)
        
        if date_from:
            events = events.filter(end_data__gte = date_from)
        else:
            events = events.filter(end_data__gte = self.event_from_filter)
        
        if date_to:
            events = events.filter(begin_date__lte = date_to)
      
        
        if uptodate:
            events = events.filter(end_data__gte = datetime.now())
        if text:
            events = events.filter(description__icontains=text)
        if sort_up:
            events = events.order_by('-begin_date')
        if sort_down:
            events = events.order_by('begin_date')


        for e in events:
            if e.begin_date < e.end_data:
                e.long = True
            else:
                e.long = False

        return events

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(EventListView, self).get_context_data(**kwargs)
        context['page_name'] = self.page_name
        context['news'] = self.news
        context['from'] = self.event_from_filter
        return context



class NewsListView(ListView):
    model = News
    template_name = 'app/news.html'
    page_name = 'news'
    events =  Event.objects.all().filter(end_data__gte = datetime.now()).order_by('begin_date')[:5]
    paginate_by = 5
    ordering = ['-publishing_date']
    
    def get_queryset(self):
        query = self.request.GET.get('title')
        if query:
            object_list = self.model.objects.filter(title__icontains=query).order_by('-publishing_date')
        else:
            object_list = self.model.objects.all().order_by('-publishing_date')
        return object_list

    def get_context_data(self, **kwargs):
        for e in self.events:
            if e.begin_date < e.end_data:
                e.long = True
            else:
                e.long = False
    
        # Call the base implementation first to get the context
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['page_name'] = self.page_name
        context['events'] = self.events
        return context

def home(request):
    return news(request)

def about(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    t = CommonText.objects.all().filter(title='О нас')
    g_str = " "
    if len(t) > 0:
        g_str = t[0].text
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
            'page_name': 'about',
            'greetings': g_str,
            'sub_page': 'news',
        }
    )


