# -*- coding: utf-8 -*-
"""
Admin config for bug tracker.
"""
from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from bug_tracker.models import Bucket, Bug, BugStatus, BugStatusHistory, BugTrackerProfile


admin.site.register(Bucket)
admin.site.register(BugStatus)
admin.site.register(BugTrackerProfile)
admin.site.register(BugStatusHistory)


class BugAdmin(OrderedModelAdmin):
    list_display = ('pk', 'move_up_down_links')

admin.site.register(Bug, BugAdmin)
