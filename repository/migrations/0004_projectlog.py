# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repository', '0003_document_official'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('actor', models.ForeignKey(related_name='actor', to=settings.AUTH_USER_MODEL)),
                ('project_log', models.ForeignKey(related_name='project_log', to='repository.Project')),
            ],
        ),
    ]
