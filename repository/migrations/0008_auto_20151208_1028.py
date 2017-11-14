# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repository', '0007_document_created_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project_Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField(max_length=255)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('actor', models.ForeignKey(related_name='actor', to=settings.AUTH_USER_MODEL, null=True)),
                ('project_log', models.ForeignKey(related_name='project_log', to='repository.Project')),
            ],
        ),
        migrations.RemoveField(
            model_name='projectlog',
            name='actor',
        ),
        migrations.RemoveField(
            model_name='projectlog',
            name='project_log',
        ),
        migrations.DeleteModel(
            name='ProjectLog',
        ),
    ]
