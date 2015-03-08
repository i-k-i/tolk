# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievement', '0002_achievementkit'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuantityAchievements',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1)),
                ('achievement', models.ForeignKey(to='achievement.Achievement')),
                ('kit', models.ForeignKey(to='achievement.AchievementKit')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='achievementkit',
            name='achievements',
        ),
    ]
