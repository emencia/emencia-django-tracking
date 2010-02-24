"""Urls for emencia.django.tracking"""
from django.conf.urls.defaults import *

from emencia.django.tracking.models import Activity

activity_all = {'queryset': Activity.objects.all()}
activity_recents = {'queryset': Activity.objects.recents()}
activity_uniques = {'queryset': Activity.objects.uniques()}
activity_inserts = {'queryset': Activity.objects.inserts()}
activity_changes = {'queryset': Activity.objects.changes()}
activity_recent_inserts = {'queryset': Activity.objects.recent_inserts()}
activity_recent_changes = {'queryset': Activity.objects.recent_changes()}
activity_recent_uniques = {'queryset': Activity.objects.recent_uniques()}

urlpatterns = patterns('django.views.generic.list_detail',
                       url(r'^$',
                           'object_list', activity_recent_uniques,
                           'tracking_activity_list'),
                       url(r'^all/$',
                           'object_list', activity_all,
                           'tracking_activity_list_all'),
                       url(r'^inserts/$',
                           'object_list', activity_inserts,
                           'tracking_activity_list_inserts'),
                       url(r'^changes/$',
                           'object_list', activity_changes,
                           'tracking_activity_list_changes'),
                       url(r'^recents/$',
                           'object_list', activity_recents,
                           'tracking_activity_list_recents'),
                       url(r'^uniques/$',
                           'object_list', activity_uniques,
                           'tracking_activity_list_uniques'),
                       url(r'^recent_inserts/$',
                           'object_list', activity_recent_inserts,
                           'tracking_activity_list_recent_inserts'),
                       url(r'^recent_changes/$',
                           'object_list', activity_recent_changes,
                           'tracking_activity_list_recent_changes'),
                       )

