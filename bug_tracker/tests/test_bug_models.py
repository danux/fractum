# -*- coding: utf-8 -*-
"""
Tests the models for creating a bug report.
"""
from django.conf import settings
from django.test import override_settings
from mock import patch
from bug_tracker.models import Bug, BugStatus
from bug_tracker.tests.test_bug_views import CreateData


class BugModelTestCase(CreateData):
    """
    Tests the bug model.
    """

    def test_can_generate_slug(self):
        """
        Tests that a slug can be generated.
        """
        bug = Bug(pk=1, bucket=self.bucket, ip_address='127.0.0.1')
        bug.generate_slug()
        self.assertEqual('{0}-{1}'.format(self.bucket.key, bug.pk), bug.slug)

    @override_settings(INITIAL_STATUS_PK=1)
    def test_can_set_initial_status(self):
        """
        The initial status of an issue should be set according the PK in the settings file.
        """
        bug = Bug(bucket=self.bucket, ip_address='127.0.0.1', pk=1)
        bug.set_initial_status(bug_tracker_profile=self.user.bug_tracker_profile)
        self.assertEqual(bug.get_status().pk, 1)

    @patch('bug_tracker.models.Bug.generate_slug')
    @patch('bug_tracker.models.Bug.set_initial_status')
    def test_creating_bug_creates_key_and_slug(self, mocked_set_initial_status, mocked_generate_slug):
        """
        Tests that when a bug is created it calls method to create key.
        """
        Bug.objects.create(
            bucket=self.bucket, ip_address='127.0.0.1', bug_tracker_profile=self.user.bug_tracker_profile
        )
        self.assertEqual(1, mocked_set_initial_status.call_count)
        self.assertEqual(1, mocked_generate_slug.call_count)


class BugTransitionTestCase(CreateData):
    """
    Tests that a bug can transition.
    """
    def test_can_transition_status(self):
        """
        Test bug's status can be transitioned.
        """
        bug = Bug.objects.create(
            bucket=self.bucket, ip_address='127.0.0.1', bug_tracker_profile=self.user.bug_tracker_profile
        )
        status = BugStatus.objects.get(pk=settings.STATUS_PKS['investigating'])
        bug.transition(status, self.user.bug_tracker_profile)
        self.assertEqual(bug.get_status().bug_status, status)
