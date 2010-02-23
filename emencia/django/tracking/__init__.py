"""emencia.django.tracking"""
import sys
import inspect

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from emencia.django.tracking.tracking import Tracker
from emencia.django.tracking.tracking import TrackingOptions

tracking = Tracker()

try:
    from django.utils.importlib import import_module
except ImportError:
    def import_module(name):
        """Simple import_module"""
        __import__(name)
        return sys.modules[name]

def tracking_load_registry(*args, **kwargs):
    """Ensures the configuration module gets imported when importing tracking"""
    # This is an idea from haystack app. We need to run the code that
    # follows only once, no matter how many times the main module is imported.
    # We'll look through the stack to see if we appear anywhere and simply
    # return if we do, allowing the original call to finish.
    stack = inspect.stack()
    
    for stack_info in stack[1:]:
        if 'tracking_load_registry' in stack_info[3]:
            return

    if not hasattr(settings, 'TRACKING_REGISTRY'):
        raise ImproperlyConfigured('You must define the TRACKING_REGISTRY setting, it should be a python module path string, for example "myproject.tracking"')

    import_module(settings.TRACKING_REGISTRY)
    
tracking_load_registry()

