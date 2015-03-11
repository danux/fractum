# -*- coding: utf-8 -*-
"""
Tests the views for creating a bug report.
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from bug_tracker.forms import CommentForm, BugForm, BugTransitionForm
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from bug_tracker.models import Bucket, Bug, BugStatus


class CreateData(TestCase):
    """
    Tests the view to generate user word clouds.
    """
    fixtures = ['statuses.json', 'buckets.json']

    def setUp(self):
        super(CreateData, self).setUp()
        self.user = get_user_model().objects.create_user(username='test_user', password='test')
        self.client.login(username=self.user.username, password='test')
        self.bucket = Bucket.objects.get(key='test')


class BucketListViewTestCase(CreateData):
    """
    Tests that buckets can be listed.
    """

    def test_view_renders(self):
        """
        Tests that the list view renders
        """
        response = self.client.get(reverse('bug_tracker:bucket_list'))
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.context['view'], ListView)


class BucketDetailViewTestCase(CreateData):
    """
    Tests that bugs can be listed.
    """

    def test_view_renders(self):
        """
        Tests that the generate word cloud view renders.
        """
        response = self.client.get(reverse('bug_tracker:bucket_detail', kwargs={'key': self.bucket.key}))
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.context['view'], DetailView)
        self.assertIsInstance(response.context['bug_form'], BugForm)


class BugCreateViewTestCase(CreateData):
    """
    Tests that bugs can be created.
    """

    def test_view_renders(self):
        """
        Tests that the generate word cloud view renders.
        """
        response = self.client.get(reverse('bug_tracker:bug_create', kwargs={'key': self.bucket.key}))
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.context['view'], CreateView)
        self.assertEqual(self.bucket, response.context['bucket'])
        self.assertTemplateUsed(response, 'bug_tracker/create_bug_form.html')

    def test_invalid_bucket_gives_404(self):
        """
        If the bucket does not exist raise a 404.
        """
        response = self.client.get(reverse('bug_tracker:bug_create', kwargs={'key': 999}))
        self.assertEqual(404, response.status_code)

    def test_submitting_form_creates_bug(self):
        """
        Tests that submitting the form creates a bug.
        """
        data = {'report': 'Test report', 'reference': 'Reference'}
        response = self.client.post(
            reverse('bug_tracker:bug_create', kwargs={'key': self.bucket.key}),
            data=data,
            follow=True,
            **{'HTTP_USER_AGENT': 'user-agent', 'REMOTE_ADDR': '127.0.0.1'}
        )
        bug = self.bucket.bug_set.get_latest()
        self.assertEqual('user-agent', bug.browser)
        self.assertEqual('127.0.0.1', bug.ip_address)
        self.assertEquals(
            'Issue {0} has been saved. Someone will review it shortly.'.format(bug.slug),
            list(response.context['messages'])[0].message
        )


class BugUpdateViewTestCase(CreateData):
    """
    Tests that bugs can be created.
    """

    def setUp(self):
        super(BugUpdateViewTestCase, self).setUp()
        self.bug = Bug.objects.create(
            bucket=self.bucket, ip_address='127.0.0.1', bug_tracker_profile=self.user.bug_tracker_profile
        )

    def test_view_renders(self):
        """
        Tests that the generate word cloud view renders.
        """
        response = self.client.get(reverse('bug_tracker:bug_update', kwargs={'slug': self.bug.slug}))
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.context['view'], UpdateView)
        self.assertTemplateUsed(response, 'bug_tracker/edit_bug_form.html')

    def test_submitting_form_edits_bug(self):
        """
        Tests that submitting the form edits a bug.
        """
        data = {'report': 'Test report', 'reference': 'Reference'}
        response = self.client.post(
            reverse('bug_tracker:bug_update', kwargs={'slug': self.bug.slug}),
            data=data,
            follow=True
        )
        self.assertEquals(
            'Issue {0} has been updated.'.format(self.bug.slug),
            list(response.context['messages'])[0].message
        )


class BugDetailViewTestCase(CreateData):
    """
    Tests for the bug detail view.
    """

    def test_has_comment_form(self):
        """
        Tests the detail view has a comment form
        """
        bug = Bug.objects.create(
            bucket=self.bucket, ip_address='127.0.0.1', bug_tracker_profile=self.user.bug_tracker_profile
        )
        response = self.client.get(bug.get_absolute_url())
        self.assertIsInstance(response.context['comment_form'], CommentForm)

    def test_has_bug_form(self):
        """
        Tests the detail view has a comment form
        """
        bug = Bug.objects.create(
            bucket=self.bucket, ip_address='127.0.0.1', bug_tracker_profile=self.user.bug_tracker_profile
        )
        response = self.client.get(bug.get_absolute_url())
        self.assertIsInstance(response.context['create_bug_form'], BugForm)
        self.assertIsInstance(response.context['edit_bug_form'], BugForm)


class CommentCreateViewTestCase(CreateData):
    """
    Tests that users can comment on bugs.
    """
    def setUp(self):
        super(CommentCreateViewTestCase, self).setUp()
        self.bug = Bug.objects.create(
            bucket=self.bucket, ip_address='127.0.0.1', bug_tracker_profile=self.user.bug_tracker_profile
        )

    def test_view_renders(self):
        """
        Tests that the view renders.
        """
        response = self.client.get(reverse('bug_tracker:comment_create', kwargs={'slug': self.bug.slug}))
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.context['view'], CreateView)
        self.assertEqual(self.bug, response.context['bug'])

    def test_can_create_comment(self):
        """
        Tests a bug can be create.
        """
        valid_data = {
            'comment': 'This is a comment.'
        }
        response = self.client.post(
            reverse('bug_tracker:comment_create', kwargs={'slug': self.bug.slug}),
            data=valid_data,
            follow=True,
        )
        self.assertRedirects(response, self.bug.get_absolute_url())
        self.assertEquals(
            'Your comment has been saved.',
            list(response.context['messages'])[0].message
        )


class TransitionViewTestCase(CreateData):
    """
    Tests that bugs can be transitioned.
    """
    def setUp(self):
        super(TransitionViewTestCase, self).setUp()
        self.bug = Bug.objects.create(
            bucket=self.bucket, ip_address='127.0.0.1', bug_tracker_profile=self.user.bug_tracker_profile
        )
        self.bug_status = BugStatus.objects.get(pk=settings.STATUS_PKS['investigating'])

    def test_transition_view_renders(self):
        """
        Tests the transition view renders.
        """
        response = self.client.get(
            reverse('bug_tracker:bug_transition', kwargs={'slug': self.bug.slug, 'status_pk': self.bug_status.pk})
        )
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.context['view'], FormView)
        self.assertIsInstance(response.context['form'], BugTransitionForm)
        self.assertEqual(self.bug, response.context['bug'])
        self.assertEqual(self.bug_status, response.context['bug_status'])
