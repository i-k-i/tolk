# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from redactor.fields import RedactorField
from time import time
from django.utils.encoding import python_2_unicode_compatible

from achievement.models import AchievementKit


def get_upload_file_name(instace, filename):
    print instace, filename
    return "uploaded_files/{}_{}".format(str(time()).replace('.','_'), filename)

@python_2_unicode_compatible
class Project(models.Model):
    name = models.CharField(max_length=200, default=str(timezone.now()))
    startdate = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User)
    description = models.TextField(default='Just one more thing')
    status = models.CharField(max_length=50, default='dreams')
    public = models.BooleanField(default=True)

    class Meta:
        permissions = (
            ('view_project', 'View project'),
            ('edit_project', 'Edit project'),
            ('comment_project', 'Comment project'),
            ('create_task', 'Create tasks')
        )
    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, related_name='creator', default=1)
    start_date = models.DateTimeField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, default='dreams')
    expected_time = models.TimeField(null=True, blank=True)
    finish_date = models.DateTimeField(null=True, blank=True)
#    real_time = models.TimeField(null=True, blank=True)
    workers = models.ManyToManyField(User, related_name='workers', null=True)
    location = models.CharField(max_length=200, default='earth')
    project = models.ForeignKey(Project)
    description = models.TextField(max_length=600, default='to do')
    tags = TaggableManager(blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    parent_task = models.ForeignKey('self', null=True, blank=True, related_name='subtask')
    digress = models.PositiveIntegerField(blank=True, null=True) # in seconds; if useful: change other TimeFields
    achievements = models.ForeignKey(AchievementKit, null=True)


    class Meta:
        permissions = (
            ('view_task', 'View task'),
            ('accept_task', 'Accept task'),
            ('done_task', 'Done task'),
            ('finish_task', 'Finish task'),
            ('create_subtask', 'Create subtask'),
            ('edit_task', 'Edit task'),
            ('comment_task', 'Comment task'),
            ('stop_task', 'Stop task'),
            ('return_task', 'Return task'),
        )

    def __unicode__(self):
        return u'{}'.format(self.name)

    def __str__(self):
        return u'{}'.format(self.name)

class ProjectComment(models.Model):
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project)
    comment = models.TextField(default='')


class TaskComment(models.Model):
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task)
    comment = RedactorField()

    def __unicode__(self):
        return u'{} | {}'.format(self.task.name, self.comment)

class ProjectorLog(models.Model):
    action_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task, blank=True, null=True)
    project = models.ForeignKey(Project, blank=True, null=True)
    message = models.TextField()
    object_name = models.CharField(max_length=200)

class Skills(models.Model):
    pass