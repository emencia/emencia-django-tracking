"""Models for emencia.django.activity"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

INSERT = 1
CHANGE = 2

class Activity(models.Model):
    ACTION_CHOICES = ((INSERT, _('insertion')),
                      (CHANGE, _('changement')),)

    action = models.IntegerField(_('action type'), choices=ACTION_CHOICES)

    title = models.CharField(_('title'), max_length=250)
    description = models.TextField(_('description'), blank=True)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)

    class Meta:
        ordering = ('creation_date',)
        verbose_name = _('activity')
        verbose_name_plural = _('activities')


