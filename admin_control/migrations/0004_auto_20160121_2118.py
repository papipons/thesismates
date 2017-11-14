# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_control', '0003_remove_course_faculty_assignment_accepted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=50)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='program',
            field=models.ForeignKey(related_name='program', default=1, to='admin_control.Program'),
            preserve_default=False,
        ),
    ]
