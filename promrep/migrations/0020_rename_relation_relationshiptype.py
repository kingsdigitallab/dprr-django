# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promrep', '0019_change_postassertion_person_relatedname'),
    ]

    operations = [
        migrations.RenameModel('Relationship', 'RelationshipType'),
    ]
