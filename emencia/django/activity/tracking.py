"""Tracking for emencia.django.activity"""
from django.db.models.signals import pre_save


class TrackingOptions(object):
    title_fields = ('__unicode__',)
    description_fields = ('__unicode__',)

    def save(self, sender, instance, **kwargs):
        import pdb; pdb.set_trace()
        
        
class Tracker(object):

    def __init__(self):
        self.registery = {}
        super(Tracker, self).__init__()
        
    
    def register(self, model, tracking_class=None):
        if not tracking_class:
            tracking_class = TrackingOptions
        
        self.registery[model] = tracking_class()
        pre_save.connect(tracking_class.save, sender=model)


tracking = Tracker()


