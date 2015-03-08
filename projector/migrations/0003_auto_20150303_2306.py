# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projector', '0002_auto_20150220_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(default=b'2015-03-03 20:06:53.852793+00:00', max_length=200),
            preserve_default=True,
        ),
    ]
