# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_control', '0003_remove_course_faculty_assignment_accepted'),
        ('repository', '0008_auto_20151208_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project_Adviser_Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField(default=False)),
                ('requested', models.ForeignKey(related_name='requested', to='admin_control.Course_Faculty_Assignment')),
                ('requester', models.ForeignKey(related_name='requester', to='repository.Project')),
            ],
        ),
    ]
