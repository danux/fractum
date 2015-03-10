# coding: utf-8
"""
Serializers for API.
"""
from rest_framework import serializers
from bug_tracker.models import Bug, Bucket


class BucketSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the UserWordCloud model.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='bug_tracker:bucket-detail'
    )

    class Meta:
        model = Bucket
        fields = (
            'pk', 'url', 'key', 'date_created', 'date_updated'
        )



class BugSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the UserWordCloud model.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='bug_tracker:bug-detail'
    )

    class Meta:
        model = Bug
        fields = (
            'pk', 'reference', 'report', 'url', 'key', 'slug', 'browser', 'ip_address', 'date_created', 'date_updated'
        )
