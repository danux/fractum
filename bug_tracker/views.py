# -*- coding: utf-8 -*-
"""
Tag cloud generator views.
"""
from django.contrib import messages
from django.forms import Form
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from bug_tracker.forms import BugForm, CommentForm, BugTransitionForm
from bug_tracker.models import Bug, Bucket, Comment, BugStatus
from bug_tracker.serializers import BugSerializer, BucketSerializer


class BucketListView(ListView):
    """
    Lists the buckets a user can view.
    """
    model = Bucket


class BugCreateView(CreateView):
    """
    View for creating a tag cloud.
    """
    model = Bug
    form_class = BugForm
    template_name = 'bug_tracker/create_bug_form.html'

    def __init__(self):
        super(BugCreateView, self).__init__()
        self.bucket = None
        self.bucket_key = None
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        self.bucket_key = kwargs['key']
        return super(BugCreateView, self).dispatch(request, *args, **kwargs)

    def get_bucket(self):
        """
        Loads the object
        """
        return Bucket.objects.get(key=self.bucket_key)

    def get_context_data(self, **kwargs):
        """
        Adds the bucket to the response context
        :type kwargs: {}
        """
        context = super(BugCreateView, self).get_context_data(**kwargs)
        context['bucket'] = self.get_bucket()
        return context

    def form_valid(self, form):
        """
        Sets the bucket, IP Address and browser for the bug.
        :type form: BugForm
        """
        self.object = form.save(commit=False)
        self.object.bug_tracker_profile = self.request.user.bug_tracker_profile
        self.object.bucket = self.get_bucket()
        self.object.browser = self.request.META['HTTP_USER_AGENT']
        self.object.ip_address = self.request.META['REMOTE_ADDR']
        self.object.save()
        messages.success(
            self.request,
            'Issue {0} has been saved. Someone will review it shortly.'.format(self.object.slug)
        )
        return super(BugCreateView, self).form_valid(form)


class BugUpdateView(UpdateView):
    """
    Allows a bug to be updated.
    """
    queryset = Bug.objects.all()
    form_class = BugForm
    template_name = 'bug_tracker/edit_bug_form.html'

    def form_valid(self, form):
        """
        Sets success message
        :type form: BugForm
        """
        messages.success(
            self.request,
            'Issue {0} has been updated.'.format(self.object.slug)
        )
        return super(BugUpdateView, self).form_valid(form)


class BucketDetailView(DetailView):
    """
    Lists bugs.
    """
    model = Bucket
    slug_field = 'key'
    slug_url_kwarg = 'key'

    def get_context_data(self, **kwargs):
        """
        Adds the bug form to the response context
        :type kwargs: {}
        """
        context = super(BucketDetailView, self).get_context_data(**kwargs)
        context['bug_form'] = BugForm()
        return context


class BugDetailView(DetailView):
    """
    View for creating a tag cloud.
    """
    model = Bug

    def get_context_data(self, **kwargs):
        """
        Adds the comment form to the context.
        """
        context = super(BugDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['create_bug_form'] = BugForm()
        context['edit_bug_form'] = BugForm(instance=self.get_object())
        return context


class CommentCreateView(CreateView):
    """
    Allows users to comment on bugs.
    """
    model = Comment
    form_class = CommentForm

    def __init__(self):
        super(CommentCreateView, self).__init__()
        self.bug = None
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs['slug']
        self.bug = get_object_or_404(Bug, slug=slug)
        return super(CommentCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Sets the bug and user.
        """
        self.object = form.save(commit=False)
        self.object.bug = self.bug
        self.object.bug_tracker_profile = self.request.user.bug_tracker_profile
        self.object.save()
        messages.success(
            self.request,
            'Your comment has been saved.',
        )
        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self):
        """
        Redirects back to bug.
        """
        return self.bug.get_absolute_url()

    def get_context_data(self, **kwargs):
        """
        Adds the bug to the context.
        """
        context_data = super(CommentCreateView, self).get_context_data(**kwargs)
        context_data['bug'] = self.bug
        return context_data


class BugTransitionFormView(FormView):
    """
    View for making transition through views.
    """
    form_class = BugTransitionForm
    template_name = 'bug_tracker/transition_bug_form.html'

    def __init__(self):
        super(BugTransitionFormView, self).__init__()
        self.bug = None
        self.bug_status = None

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs['slug']
        status_pk = kwargs['status_pk']
        self.bug = get_object_or_404(Bug, slug=slug)
        self.bug_status = get_object_or_404(BugStatus, pk=status_pk)
        return super(BugTransitionFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adds the bug and status to the response context
        :type kwargs: {}
        """
        context = super(BugTransitionFormView, self).get_context_data(**kwargs)
        context['bug'] = self.bug
        context['bug_status'] = self.bug_status
        return context

    def form_valid(self, form):
        """
        Sets the bucket, IP Address and browser for the bug.
        :type form: BugForm
        """
        status_before = self.bug.get_status().bug_status
        self.bug.transition(bug_status=self.bug_status, bug_tracker_profile=self.request.user.bug_tracker_profile)
        self.bug.save()
        Comment.objects.create(
            comment=form.cleaned_data['comment'],
            bug_tracker_profile=self.request.user.bug_tracker_profile,
            bug=self.bug,
            status_before=status_before,
            status_after=self.bug_status,
        )
        messages.success(
            self.request,
            'Status set to {0}.'.format(self.bug_status.title)
        )
        return super(BugTransitionFormView, self).form_valid(form)

    def get_success_url(self):
        """
        Redirects to the bug
        """
        return self.bug.get_absolute_url()


@api_view(('GET',))
def api_root(request, response_format=None):
    """
    Provides a root to the API.
    :type response_format: unicode
    """
    return Response({
        'bugs': reverse('bug_tracker:bug-list', request=request, format=response_format),
        'buckets': reverse('bug_tracker:bucket-list', request=request, format=response_format),
    })


class BugApiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Bug API views.
    """
    queryset = Bug.objects.all()
    paginate_by = 10
    serializer_class = BugSerializer


class BucketApiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Bug API views.
    """
    queryset = Bucket.objects.all()
    paginate_by = 10
    serializer_class = BucketSerializer
