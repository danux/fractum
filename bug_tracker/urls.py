# -*- coding: utf-8 -*-
"""
URLs for the word cloud app.
"""
from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from bug_tracker.views import api_root, BugCreateView, BugDetailView, BugApiViewSet, BucketDetailView, BucketApiViewSet
from bug_tracker.views import BucketListView, CommentCreateView, BugUpdateView, BugTransitionFormView


urlpatterns = patterns(
    '',
    url(r'^$', BucketListView.as_view(), name='bucket_list'),
    url(r'^bucket/(?P<key>[\d\w]+)/$', BucketDetailView.as_view(), name='bucket_detail'),
    url(r'^bucket/(?P<key>[\d\w]+)/bug/create/$', BugCreateView.as_view(), name='bug_create'),
    url(r'^bug/(?P<slug>[\d\w]+\-[\d]+)/$', BugDetailView.as_view(), name='bug_detail'),
    url(
        r'^bug/(?P<slug>[\d\w]+\-[\d]+)/transition/(?P<status_pk>[\d]+)/$',
        BugTransitionFormView.as_view(),
        name='bug_transition'
    ),
    url(r'^bug/(?P<slug>[\d\w]+\-[\d]+)/transition/$', BugUpdateView.as_view(), name='bug_update'),
    url(r'^bug/(?P<slug>[\d\w]+\-[\d]+)/comment/create/$', CommentCreateView.as_view(), name='comment_create'),
)


urlpatterns += format_suffix_patterns([
    url(r'^api/$', api_root, name='api_root')
])


router = DefaultRouter()
router.register(r'api/bug', BugApiViewSet)
router.register(r'api/bucket', BucketApiViewSet)
urlpatterns += router.urls
