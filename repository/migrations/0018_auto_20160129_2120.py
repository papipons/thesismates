# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_control', '0005_auto_20160124_1320'),
        ('repository', '0017_user_docu_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='course_owner',
            field=models.ForeignKey(related_name='course_owner', blank=True, to='admin_control.Course_Faculty_Assignment', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='project_owner',
            field=models.ForeignKey(related_name='project_owner', blank=True, to='repository.Project', null=True),
        ),
    ]
