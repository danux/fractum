# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bug_tracker', '0003_bugtrackerprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='bug_tracker_profile',
            field=models.ForeignKey(default=1, to='bug_tracker.BugTrackerProfile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bugstatushistory',
            name='bug_tracker_profile',
            field=models.ForeignKey(default=1, to='bug_tracker.BugTrackerProfile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bugtrackerprofile',
            name='user',
            field=models.OneToOneField(related_name='bug_tracker_profile', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
