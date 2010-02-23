"""Tracking objects for emencia.django.tracking"""
from django.db.models.signals import post_save

from emencia.django.tracking.models import Activity
from emencia.django.tracking.models import INSERT, CHANGE

class TrackingOptions(object):
    title_fields = ('__unicode__',)
    description_fields = ('__unicode__',)

    def get_model_value(self, model_instance, field):
        """Resolve the attribute of a model"""
        value = getattr(model_instance, field)
        if callable(value):
            return value()
        return value

    def get_title_value(self, model_instance):
        """Compute the title value for Activity creation"""
        return ' '.join([self.get_model_value(model_instance, field)
                         for field in self.title_fields])[:250]

    def get_description_value(self, model_instance):
        """Compute the description value for Activity creation"""
        return '\r\n'.join([self.get_model_value(model_instance, field)
                            for field in self.description_fields])

    def get_url_value(self, model_instance):
        """Compute the url value for Activity creation"""
        try:
            return model_instance.get_absolute_url()
        except:
            return ''

    def save(self, sender, **kw):
        """Track the activity"""
        instance = kw['instance']
        created = kw['created']

        data = {'action': created and INSERT or CHANGE,
                'title': self.get_title_value(instance),
                'description': self.get_description_value(instance),
                'url': self.get_url_value(instance),
                'content_object': instance}

        activity = Activity.objects.create(**data)
        return activity

class Tracker(object):

    def __init__(self):
        self.registery = {}
        super(Tracker, self).__init__()

    def register(self, model, tracking_class=None):
        if not tracking_class:
            tracking_class = TrackingOptions

        self.registery[model] = tracking_class()
        post_save.connect(self.registery[model].save, sender=model)

