# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0019_auto_20160129_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_log',
            name='end_sy',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project_log',
            name='semester',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project_log',
            name='start_sy',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
