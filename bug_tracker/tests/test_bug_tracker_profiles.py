# -*- coding: utf-8 -*-
"""
Tests that user's bucket profiles work. Bucket profiles associate users to
Buckets and define what users can see.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from bug_tracker.models import BugTrackerProfile


class BucketProfileCreateTestCase(TestCase):
    """
    Tests when a user is created they get a bucket profile.
    """

    def test_create_user(self):
        """
        Tests when a user is created they get a bucket profile.
        """
        user = get_user_model().objects.create_user(username='bucket_profile_test')
        self.assertIsInstance(user.bug_tracker_profile, BugTrackerProfile)
