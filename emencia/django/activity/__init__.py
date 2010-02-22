"""emencia.django.activity"""
import inspect

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    # importlib support (from Python 2.7) added on r10088
    # post 1.0
    from django.utils.importlib import import_module
except ImportError:
    def import_module(name):
        """Simple import_module for Django 1.0+"""
        __import__(name)
        return sys.modules[name]

def activity_load_registry(*args, **kwargs):
    """Ensures the configuration module gets imported when importing activity"""
    # This is an idea from haystack app. We need to run the code that
    # follows only once, no matter how many times the main module is imported.
    # We'll look through the stack to see if we appear anywhere and simply
    # return if we do, allowing the original call to finish.
    stack = inspect.stack()
    
    for stack_info in stack[1:]:
        if 'activty_load_registry' in stack_info[3]:
            import pdb; pdb.set_trace()
            return

    if not hasattr(settings, 'ACTIVITY_REGISTRY'):
        raise ImproperlyConfigured('You must define the ACTIVITY_REGISTRY setting, it should be a python module path string, for example "myproject.activity_registry"')

    import_module(settings.ACTIVITY_REGISTRY)
    
activity_load_registry()

