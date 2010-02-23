"""Urls for emencia.django.tracking"""
from django.conf.urls.defaults import *

from emencia.django.tracking.models import Activity

activity_all = {'queryset': Activity.objects.all()}
activity_recents = {'queryset': Activity.objects.recents()}
activity_inserts = {'queryset': Activity.objects.insertions()}
activity_changes = {'queryset': Activity.objects.changements()}

urlpatterns = patterns('django.views.generic.list_detail',
                       url(r'^$', 'object_list',
                           activity_all, 'tracking_activity_list'),
                       url(r'^recents/$', 'object_list',
                           activity_recents, 'tracking_activity_list_recents'),
                       url(r'^inserts/$', 'object_list',
                           activity_inserts, 'tracking_activity_list_inserts'),
                       url(r'^changes/$', 'object_list',
                           activity_changes, 'tracking_activity_list_changes'),
                       )

