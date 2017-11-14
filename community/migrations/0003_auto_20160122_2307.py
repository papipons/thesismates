# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_question_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='accepted',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='question_answer',
            name='accepted',
            field=models.NullBooleanField(),
        ),
    ]
