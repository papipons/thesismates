# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_control', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_faculty_assignment',
            name='accepted',
            field=models.BooleanField(default=True),
        ),
    ]
