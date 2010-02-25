=======================
Emencia Django Tracking
=======================

The problematic was :

 *I wrote some articles, and updated many pages on my Django website, how can I inform my visitors of these updates ?*

Emencia.django.tracking allows you to track the activities of your models and display them on a timeline without
changing the models' code.

.. contents::

Features
========

Better than a long speech, here is a list of the main features :

  * No need to change your models.
  * Highly customizable.
  * Views and template tags to display the activities.

Installation
============

You can retrieve the last sources from http://github.com/Fantomas42/emencia-django-tracking and run the installation script ::

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

Now create a python module somewhere in your project, for example **tracking.py** in your project directory (let's suppose it is called "project"),
and add something like the following line to your project's settings : ::

  >>> TRACKING_REGISTRY = 'project.tracking'

In the tracking.py module we will register the models we want to track.
Imagine we have a model named *News* with a *description* and *title* field.

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

In your project urls.py add this following line to serve the views packaged in the app. ::

  >>> url(r'^tracking/', include('emencia.django.tracking.urls')),

This urlset provides many views to display these activities :

/
  Display the latest activity of each model instance tracked in a recent period.

/all/
  Display all the activities tracked.

/recents/
  Display all the recent activities tracked.

/inserts/
  Display all the creations of models tracked.

/recent_inserts/
  Display the recent creations of models tracked.

/changes/
  Display all the changes of models tracked.

/recent_changes/
  Display the recent changes of models tracked.

/uniques/
  Display all the latest activity of each model instance tracked.

Synchronization
---------------

Now you can run a *syncdb* to install the models into your database.


