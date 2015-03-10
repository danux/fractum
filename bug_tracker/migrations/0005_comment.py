# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bug_tracker', '0004_auto_20150228_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('bug', models.ForeignKey(to='bug_tracker.Bug')),
                ('bug_tracker_profile', models.ForeignKey(to='bug_tracker.BugTrackerProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
