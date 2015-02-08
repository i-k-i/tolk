#from libxslt import extensionModule
from django.db import models
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField
from hashlib import sha1

ACHIEVEMENT_IMAGE_PATH = 'achievement'
ACHIEVEMENT_IMAGE_SETTINGS = {'size': (100,100), 'crop': 'smart'}


def path_to_image(instance, filename):
    extension = filename.split('.')[-1].lower()
    new_fname = sha1(u'{}'.format(instance.name).encode('utf-8')).hexdigest()
    return '{}/{}.{}'.format(ACHIEVEMENT_IMAGE_PATH, new_fname, extension)

class Achievement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    creator = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(blank=True, null=True, upload_to='achievement')
    image = ThumbnailerImageField(blank=True,
                                  null=True,
                                  upload_to=path_to_image,
                                  resize_source=ACHIEVEMENT_IMAGE_SETTINGS,
                                  help_text=('Image of achievement.'))

    def __unicode__(self):
        return u'{}'.format(self.name)

    def __str__(self):
        return u'{}'.format(self.name)

class AchievementState(models.Model):
    achievement = models.ForeignKey(Achievement)
    user = models.ForeignKey(User)
    quantity = models.IntegerField(default=0)

class AchievementLogs(models.Model):
    achievement = models.ForeignKey(Achievement)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def get_achievement_name(self):
        return u'{}'.format(self.achievement.name)
