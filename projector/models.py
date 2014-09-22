# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from datetime import datetime

class Project(models.Model):
    name = models.CharField(max_length=200, default=str(timezone.now()))
    startdate = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    author = models.ForeignKey(User)
    description = models.TextField(default='Just one more thing')
    tags = TaggableManager()
    status = models.CharField(max_length=50, default='dreams')

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=200)
    startdate = models.DateTimeField(default=timezone.now())
    status = models.CharField(max_length=50, default='dreams')
    expected_time = models.TimeField('expected time')
    real_time = models.TimeField()
    workers = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class PrComments(models.Model):
    author = models.ForeignKey(User)
    date = models.DateTimeField('date published', default = datetime.now)
    project = models.ForeignKey(Project)

class TaskComment(models.Model):
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=timezone.now())
    task = models.ForeignKey(Task)
