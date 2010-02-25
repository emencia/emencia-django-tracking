=======================
Emencia Django Tracking
=======================

The problematic was :

 *I have wrote some articles, and updating many pages on my Django website, how can I inform my visitors for these updates ?*

Emencia.django.tracking allow you to track the activity of your models without
changing it, and display this timeline.

.. contents::

Features
========

More than a long speech, here the list of the main features :

  * No needs to change your models.
  * Highly customizable.
  * Views and template tags for displaying activities.

Installation
============

You could retrieve the last sources from http://github.com/Fantomas42/emencia-django-tracking and running the installation script ::
    
  $> python setup.py install

or use pip ::

  $> pip install -e git://github.com/Fantomas42/emencia-django-tracking.git#egg=emencia.django.tracking

Applications
------------

Then register **emencia.django.tracking** and **contenttypes** in the INSTALLED_APPS section of your project's settings. ::

  >>> INSTALLED_APPS = (
  ...   # Your favorites apps
  ...   'django.contrib.contenttypes',
  ...   'emencia.django.tracking',)

The Registry
------------

Now create a python module somewhere in your project, for example **tracking.py** in your project directory (lets suppose its called "project"), 
and add something like the following line to your project's settings : ::

  >>> TRACKING_REGISTRY = 'project.tracking'

In the tracking.py module we will register the models we want to track.
Imagine we have an model named *News* with a *description* and *title* field.

  >>> from emencia.django.tracking import tracking
  >>> from emencia.django.tracking import TrackingOptions
  >>>
  >>> from myapp.models import News
  >>>
  >>> class NewsletterTracking(TrackingOptions):
  >>>   description_fields = ('title', 'content',)
  >>>
  >>> tracking.register(Newsletter, NewsletterTracking)

Urls
----

In your project urls.py adding this following line to serve the views packaged in the app. ::

  >>> url(r'^tracking/', include('emencia.django.tracking.urls')),

This urlset provides many views for displaying the activities :

/
  Display the latest activity of each model instances tracked in a recent period.

/all/
  Display all the activities tracked.

/recents/
  Display all the recents activities tracked.
  
/inserts/
  Display the all tracked models creations

/recent_inserts/
  Display the recent tracked models creations

/changes/
  Display the all tracked models changes

/recent_changes/
  Display the recent tracked models changes

/uniques/
  Display all the latest activity of each model instances tracked.

Synchronization
---------------

Now you can run a *syncdb* for installing the models into your database.


