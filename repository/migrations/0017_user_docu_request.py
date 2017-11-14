# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repository', '0016_auto_20160114_0101'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Docu_Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('semester', models.CharField(max_length=50)),
                ('start_sy', models.CharField(max_length=50)),
                ('end_sy', models.CharField(max_length=50)),
                ('access', models.NullBooleanField()),
                ('req_docs', models.ForeignKey(related_name='req_docs', to='repository.Project')),
                ('user', models.ForeignKey(related_name='docu_requester', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
