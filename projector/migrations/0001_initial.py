# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'2015-02-08 14:43:21.221355+00:00', max_length=200)),
                ('startdate', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField(null=True, blank=True)),
                ('description', models.TextField(default=b'Just one more thing')),
                ('status', models.CharField(default=b'dreams', max_length=50)),
                ('public', models.BooleanField(default=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_project', 'View project'), ('edit_project', 'Edit project'), ('comment_project', 'Comment project'), ('create_task', 'Create tasks')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(default=b'')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='projector.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectorLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_time', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('object_name', models.CharField(max_length=200)),
                ('project', models.ForeignKey(blank=True, to='projector.Project', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(default=b'dreams', max_length=50)),
                ('expected_time', models.TimeField(null=True, blank=True)),
                ('finish_date', models.DateTimeField(null=True, blank=True)),
                ('location', models.CharField(default=b'earth', max_length=200)),
                ('description', models.TextField(default=b'to do', max_length=600)),
                ('deadline', models.DateTimeField(null=True, blank=True)),
                ('digress', models.PositiveIntegerField(null=True, blank=True)),
                ('creator', models.ForeignKey(related_name='creator', default=1, to=settings.AUTH_USER_MODEL)),
                ('parent_task', models.ForeignKey(related_name='subtask', blank=True, to='projector.Task', null=True)),
                ('project', models.ForeignKey(to='projector.Project')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('workers', models.ManyToManyField(related_name='workers', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_task', 'View task'), ('accept_task', 'Accept task'), ('done_task', 'Done task'), ('finish_task', 'Finish task'), ('create_subtask', 'Create subtask'), ('edit_task', 'Edit task'), ('comment_task', 'Comment task'), ('stop_task', 'Stop task'), ('return_task', 'Return task')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', redactor.fields.RedactorField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(to='projector.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='projectorlog',
            name='task',
            field=models.ForeignKey(blank=True, to='projector.Task', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectorlog',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
