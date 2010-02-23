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

    def recents(self):
        period = datetime.now() - timedelta(days=settings.VISIBILITY_DAYS)
        return self.get_query_set().filter(creation_date__gt=period)
                                           
    def insertions(self):
        return self.recents().filter(action=INSERT)

    def changements(self):
        return self.recents().filter(action=CHANGE)
    

class Activity(models.Model):
    ACTION_CHOICES = ((INSERT, _('insertion')),
                      (CHANGE, _('changement')),)

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
        ordering = ('creation_date',)
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
