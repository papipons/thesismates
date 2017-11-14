# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0010_auto_20151208_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_adviser_request',
            name='accepted',
            field=models.NullBooleanField(),
        ),
    ]
