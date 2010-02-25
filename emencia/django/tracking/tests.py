"""Unit tests for emencia.django.tracking"""
from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from emencia.django.tracking import tracking
from emencia.django.tracking.models import Activity
from emencia.django.tracking.models import CHANGE

class ActivityTestCase(TestCase):

    def setUp(self):
        tracking.register(User)

        self.objects = [User.objects.create_user(username, '%s@domain.com' % username)
                        for username in ['toto', 'titi', 'tata']]

    def test_manager(self):
        self.assertEquals(Activity.objects.all().count(), 3)
        self.assertEquals(Activity.objects.uniques().count(), 3)
        self.assertEquals(Activity.objects.recent_uniques().count(), 3)
        self.assertEquals(Activity.objects.inserts().count(), 3)
        self.assertEquals(Activity.objects.changes().count(), 0)
        self.assertEquals(Activity.objects.recent_inserts().count(), 3)
        self.assertEquals(Activity.objects.recent_changes().count(), 0)

        self.objects[0].username = 'toto_change'
        self.objects[0].save()
        
        self.assertEquals(Activity.objects.all().count(), 4)
        self.assertEquals(Activity.objects.uniques().count(), 3)
        self.assertEquals(Activity.objects.recent_uniques().count(), 3)
        self.assertEquals(Activity.objects.inserts().count(), 3)
        self.assertEquals(Activity.objects.changes().count(), 1)
        self.assertEquals(Activity.objects.recent_inserts().count(), 3)
        self.assertEquals(Activity.objects.recent_changes().count(), 1)

        activity = Activity.objects.get(pk=2)
        activity.creation_date = datetime(2000, 1, 1)
        activity.save()

        self.assertEquals(Activity.objects.all().count(), 4)
        self.assertEquals(Activity.objects.uniques().count(), 3)
        self.assertEquals(Activity.objects.recent_uniques().count(), 2)
        self.assertEquals(Activity.objects.inserts().count(), 3)
        self.assertEquals(Activity.objects.changes().count(), 1)
        self.assertEquals(Activity.objects.recent_inserts().count(), 2)
        self.assertEquals(Activity.objects.recent_changes().count(), 1)
