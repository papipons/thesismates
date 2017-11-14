# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0012_user_last_visit_ongoing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_last_visit_ongoing',
            name='last_visit',
            field=models.DateTimeField(null=True),
        ),
    ]
