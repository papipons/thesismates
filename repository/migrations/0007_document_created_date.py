# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0006_auto_20151126_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
