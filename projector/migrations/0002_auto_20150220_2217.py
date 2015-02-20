# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievement', '0002_achievementkit'),
        ('projector', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='achievements',
            field=models.ForeignKey(to='achievement.AchievementKit', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(default=b'2015-02-20 19:17:38.085085+00:00', max_length=200),
            preserve_default=True,
        ),
    ]
