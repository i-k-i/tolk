from django.db import models
from django.contrib.auth.models import User

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, upload_to='/achivement')

    def __str__(self):
        return self.name

class AchievementState(models.Model):
    achievement = models.ForeignKey(Achievement)
    user = models.ForeignKey(User)
    count = models.IntegerField(default=1)

class AchievementLogs(models.Model):
    achievement = models.ForeignKey(Achievement)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
