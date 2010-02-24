"""Models for emencia.django.tracking"""
from datetime import datetime
from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from emencia.django.tracking import settings

INSERT = 1
CHANGE = 2

class ActivityManager(models.Manager):

    def inserts(self):
        return self.get_query_set().filter(action=INSERT)

    def changes(self):
        return self.get_query_set().filter(action=CHANGE)

    def recents(self):
        period = datetime.now() - timedelta(days=settings.VISIBILITY_DAYS)
        return self.get_query_set().filter(creation_date__gt=period)
    
    def recent_inserts(self):
        return self.recents().filter(action=INSERT)

    def recent_changes(self):
        return self.recents().filter(action=CHANGE)

    def get_last_activity_model_ids(self):
        objects = set(self.get_query_set().values_list('content_type', 'object_id'))
        ids = []
        for obj in objects:
            last_activity = self.get_query_set().filter(content_type=obj[0],
                                                        object_id=obj[1]).latest('creation_date')
            ids.append(last_activity.id)
        return ids

    def uniques(self):
        ids = self.get_last_activity_model_ids()
        return self.get_query_set().filter(id__in=ids)

    def recent_uniques(self):
        ids = self.get_last_activity_model_ids()
        return self.recents().filter(id__in=ids)
        
        

class Activity(models.Model):
    ACTION_CHOICES = ((INSERT, _('insert')),
                      (CHANGE, _('change')),)

    action = models.IntegerField(_('action type'), choices=ACTION_CHOICES)

    title = models.CharField(_('title'), max_length=250)
    description = models.TextField(_('description'), blank=True)
    url = models.CharField(_('url'), max_length=250, blank=True)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)

    objects = ActivityManager()

    def __unicode__(self):
        return '%s %s' % (self.content_type.model.capitalize(),
                          self.title)

    def get_absolute_url(self):
        return self.url

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
