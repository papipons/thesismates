# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0015_auto_20160102_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.TextField(),
        ),
    ]
