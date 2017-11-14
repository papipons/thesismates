# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repository', '0014_auto_20160101_2339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event_Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(related_name='event', to='repository.Event')),
                ('member', models.ForeignKey(related_name='included_member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='included_members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='repository.Event_Actor'),
        ),
    ]
