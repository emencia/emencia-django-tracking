"""emencia.django.tracking"""
import sys
import inspect
import warnings

from django.conf import settings as project_settings
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
    stack = inspect.stack()

    for stack_info in stack[1:]:
        if 'tracking_load_registry' in stack_info[3]:
            return

    if not hasattr(project_settings, 'TRACKING_REGISTRY'):
        warnings.warn('You must define the TRACKING_REGISTRY setting, it should be a python module path string, for example "myproject.tracking"')
        return

    if project_settings.TRACKING_REGISTRY:
        import_module(project_settings.TRACKING_REGISTRY)

tracking_load_registry()

