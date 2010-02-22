"""Tracking for emencia.django.activity"""
from django.db.models.signals import post_save

from emencia.django.activity.models import Activity
from emencia.django.activity.models import INSERT, CHANGE

def get_value(instance, field):
    value = getattr(instance, field)
    if callable(value):
        return value()
    return value

class TrackingOptions(object):
    title_fields = ('__unicode__',)
    description_fields = ('__unicode__',)

    def save(self, sender, **kw):
        instance = kw['instance']
        created = kw['created']

        data = {'action': created and INSERT or CHANGE,
                'title': ' '.join([get_value(instance, field)
                                   for field in self.title_fields])[:250],
                'description': '\r\n'.join([get_value(instance, field)
                                            for field in self.description_fields]),
                'content_object': instance}

        activity = Activity.objects.create(**data)
        return data
                
class Tracker(object):

    def __init__(self):
        self.registery = {}
        super(Tracker, self).__init__()
        
    
    def register(self, model, tracking_class=None):
        if not tracking_class:
            tracking_class = TrackingOptions
        
        self.registery[model] = tracking_class()
        post_save.connect(self.registery[model].save, sender=model)


tracking = Tracker()
