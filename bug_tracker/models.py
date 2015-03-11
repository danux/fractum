# -*- coding: utf-8 -*-
"""
Models for a bug tracker.
"""
from __future__ import unicode_literals
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from ordered_model.models import OrderedModel


class BugTrackerProfile(models.Model):
    """
    Associates users to the bug tracker app.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='bug_tracker_profile')


def create_bug_tracker_profile(sender, **kwargs):
    """
    Generates a key and slug for new bugs.
    :type sender: Bug
    :type kwargs: {}
    """
    del sender
    instance = kwargs['instance']
    if kwargs['created']:
        BugTrackerProfile.objects.create(user=instance)
post_save.connect(create_bug_tracker_profile, sender=settings.AUTH_USER_MODEL)


class Bucket(models.Model):
    """
    A bucket is a collection of bugs.
    """
    title = models.CharField(max_length=255)
    key = models.CharField(max_length=5, unique=True, db_index=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('bug_tracker:bucket_detail', kwargs={'key': self.key})


class BugStatus(models.Model):
    """
    Represents the status of a bug in the workflow.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class BugManager(models.Manager):
    """
    Manager for Bug model.
    """
    def get_latest(self):
        """
        Gets the latest bug according to the key.
        """
        try:
            return self.order_by('-date_created')[0]
        except IndexError:
            raise self.model.DoesNotExist


class Bug(OrderedModel):
    """
    A bug is reported by a user and lives in a bucket.
    """
    slug = models.CharField(max_length=150, unique=True, blank=True, null=True)
    bucket = models.ForeignKey(Bucket)
    reference = models.CharField(max_length=255)
    report = models.TextField()
    url = models.CharField(max_length=500, blank=True, null=True)
    browser = models.CharField(max_length=1000)
    ip_address = models.IPAddressField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    bug_tracker_profile = models.ForeignKey(BugTrackerProfile)

    order_with_respect_to = 'bucket'
    objects = BugManager()

    def get_status(self):
        """
        Returns the latest status
        """
        return self.bugstatushistory_set.get_latest()

    def generate_slug(self):
        """
        Generates a slug from the bucket key and the bug key.
        """
        self.slug = '{0}-{1}'.format(self.bucket.key, self.pk)

    def set_initial_status(self, bug_tracker_profile):
        """
        Sets the bug's status to the status with a pk matching INITIAL_STATUS_PK.
        """
        bug_status = BugStatus.objects.get(pk=settings.INITIAL_STATUS_PK)
        self.transition(bug_status=bug_status, bug_tracker_profile=bug_tracker_profile)

    def get_absolute_url(self):
        """
        Sets the absolute URL of the Bug.
        """
        return reverse('bug_tracker:bug_detail', kwargs={'slug': self.slug})

    def transition(self, bug_status, bug_tracker_profile):
        """
        Transitions a bug to a new status.
        """
        BugStatusHistory.objects.create(bug_status=bug_status, bug=self, bug_tracker_profile=bug_tracker_profile)


def generate_key(sender, **kwargs):
    """
    Generates a key and slug for new bugs.
    :type sender: Bug
    :type kwargs: {}
    """
    del sender
    instance = kwargs['instance']
    if kwargs['created']:
        instance.generate_slug()
        instance.set_initial_status(instance.bug_tracker_profile)
        instance.save()
post_save.connect(generate_key, sender=Bug)


class BugStatusHistoryManager(models.Manager):
    """
    Manages the BugStatusHistory model
    """
    def get_latest(self):
        """
        Returns the BugStatusHistory with the most recent date_created.
        """
        return self.order_by('-date_created')[0]


class BugStatusHistory(models.Model):
    """
    Represents a Bug and a BugStatus at given point in history.
    """
    bug = models.ForeignKey(Bug)
    bug_status = models.ForeignKey(BugStatus)
    bug_tracker_profile = models.ForeignKey(BugTrackerProfile)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = BugStatusHistoryManager()

    class Meta(object):
        """
        Meta properties.
        """
        ordering = ['-date_created']


class Comment(models.Model):
    """
    Allows users to comment on bugs.
    """
    bug = models.ForeignKey(Bug)
    bug_tracker_profile = models.ForeignKey(BugTrackerProfile)
    comment = models.TextField(null=True)
    status_before = models.ForeignKey(BugStatus, related_name='+', null=True)
    status_after = models.ForeignKey(BugStatus, related_name='+', null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        """
        Meta properties.
        """
        ordering = ['date_created']
