# -*- coding: utf-8 -*-
"""
Bug report forms.
"""
from django import forms
from bug_tracker.models import Bug, Comment


class CommentForm(forms.ModelForm):
    """
    Form for creating a comment.
    """
    class Meta(object):
        """
        Meta options.
        """
        model = Comment
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
        fields = ['comment']


class BugForm(forms.ModelForm):
    """
    Model form for creating a bug.
    """
    class Meta(object):
        """
        Meta options.
        """
        model = Bug
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'report': forms.Textarea(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ['reference', 'report', 'url']


class BugTransitionForm(forms.Form):
    """
    Bug transition form
    """
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
