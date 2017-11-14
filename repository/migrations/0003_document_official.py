# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_document_uploaded_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='official',
            field=models.BooleanField(default=False),
        ),
    ]
