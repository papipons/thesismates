# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_projectlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectlog',
            name='message',
            field=models.TextField(max_length=255),
        ),
    ]
