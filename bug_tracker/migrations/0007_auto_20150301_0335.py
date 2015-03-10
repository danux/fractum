# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bug_tracker', '0006_auto_20150301_0327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status_after',
            field=models.ForeignKey(related_name='+', to='bug_tracker.BugStatus', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='status_before',
            field=models.ForeignKey(related_name='+', to='bug_tracker.BugStatus', null=True),
            preserve_default=True,
        ),
    ]
