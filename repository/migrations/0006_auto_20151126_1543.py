# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_auto_20151126_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectlog',
            name='actor',
            field=models.ForeignKey(related_name='actor', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
