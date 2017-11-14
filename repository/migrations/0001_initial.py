# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import repository.models
import django.utils.timezone
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('admin_control', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to=repository.models.generate_filename)),
                ('mime_type', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('start_time', models.TimeField(null=True, blank=True)),
                ('end_time', models.TimeField(null=True, blank=True)),
                ('event_type', models.CharField(max_length=50, null=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('posted_by', models.ForeignKey(related_name='posted_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('abstract', models.TextField(max_length=200, null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(null=True, blank=True)),
                ('secret_code', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('status', models.CharField(default=b'ongoing', max_length=200)),
                ('adviser', models.ForeignKey(related_name='adviser', blank=True, to='admin_control.Course_Faculty_Assignment', null=True)),
                ('coordinator', models.ForeignKey(related_name='coordinator', to='admin_control.Course_Faculty_Assignment')),
            ],
        ),
        migrations.CreateModel(
            name='Project_Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('member', models.ForeignKey(related_name='member', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(related_name='project', to='repository.Project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='repository.Project_Membership'),
        ),
        migrations.AddField(
            model_name='event',
            name='project_owner',
            field=models.ForeignKey(related_name='project_owner', to='repository.Project'),
        ),
        migrations.AddField(
            model_name='document',
            name='owner',
            field=models.ForeignKey(related_name='owner', to='repository.Project'),
        ),
    ]
