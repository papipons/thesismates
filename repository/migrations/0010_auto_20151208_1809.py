# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0009_project_adviser_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_adviser_request',
            name='accepted',
            field=models.BooleanField(),
        ),
    ]
