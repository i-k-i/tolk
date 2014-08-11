# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=200, default=str(timezone.now()))
    startdate = models.DateTimeField(default=timezone.now())
    deadline = models.DateTimeField(default=timezone.now()+10)
    author = models.ForeignKey(User)
    description = models.TextField(default='Just one more thing')
    tags = TaggableManager()
    status =
    comments =


    def __str__(self):
        return self.name

#class PrStatus(models):

class Task(models.Model):
    name = models.CharField(max_length=200)
    startdate = models.DateTimeField(default=timezone.now())


class PrComments(models.Model):
    author=