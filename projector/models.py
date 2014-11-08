# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from filer.fields.image import FilerImageField

from datetime import datetime

from redactor.fields import RedactorField

from time import time


def get_upload_file_name(instace, filename):
    print instace, filename

  #  return "uploaded_files/{}_{}".format(str(time()).replace('.','_'), filename)
    return "uploaded_files/{}_{}".format(str(time()).replace('.','_'), filename)


class Project(models.Model):
    name = models.CharField(max_length=200, default=str(timezone.now()))
    startdate = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User)
    description = models.TextField(default='Just one more thing')
    status = models.CharField(max_length=50, default='dreams')

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User,related_name='creator', default=1)
    start_date = models.DateTimeField(blank=True, null=True)
 #   create_date = models.DateTimeField(auto_now_add=True, null=True)
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
    comment = RedactorField(verbose_name=u'Text')
#    comment = models.TextField(default='')
#    image = FilerImageField(null=True, blank=True)

#    file = models.FileField(upload_to=get_upload_file_name, null=True, blank=True)

#    def __str__(self):
#        return 'Task comment'

#    def __unicode__(self):
#        return u"%s" % self

class Skills(models.Model):
    pass