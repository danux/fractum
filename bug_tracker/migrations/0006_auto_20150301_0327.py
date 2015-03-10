# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bug_tracker', '0005_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bugstatushistory',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date_created']},
        ),
        migrations.AddField(
            model_name='comment',
            name='status_after',
            field=models.OneToOneField(related_name='+', null=True, to='bug_tracker.BugStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='status_before',
            field=models.OneToOneField(related_name='+', null=True, to='bug_tracker.BugStatus'),
            preserve_default=True,
        ),
    ]
