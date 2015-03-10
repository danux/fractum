# -*- coding: utf-8 -*-
"""
Master URLs file.
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^', include('bug_tracker.urls', namespace='bug_tracker')),
    url(r'^admin/', include(admin.site.urls)),
)
