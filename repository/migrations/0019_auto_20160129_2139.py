# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_control', '0005_auto_20160124_1320'),
        ('repository', '0018_auto_20160129_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_log',
            name='course_log',
            field=models.ForeignKey(related_name='course_log', blank=True, to='admin_control.Course_Faculty_Assignment', null=True),
        ),
        migrations.AlterField(
            model_name='project_log',
            name='project_log',
            field=models.ForeignKey(related_name='project_log', blank=True, to='repository.Project', null=True),
        ),
    ]
