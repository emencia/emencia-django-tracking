"""Settings for emencia.django.tracking"""
from django.conf import settings

VISIBILITY_DAYS = getattr(settings, 'TRACKING_VISIBILITY_DAYS', 60)
