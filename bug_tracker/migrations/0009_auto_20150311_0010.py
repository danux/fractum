# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bug_tracker', '0008_auto_20150301_0400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bug',
            name='key',
        ),
        migrations.AlterField(
            model_name='bucket',
            name='key',
            field=models.CharField(unique=True, max_length=5, db_index=True),
            preserve_default=True,
        ),
    ]
