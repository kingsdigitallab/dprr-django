# -*- coding: utf-8 -*-


from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("promrep", "0019_change_postassertion_person_relatedname"),
    ]

    operations = [
        migrations.RenameModel("Relationship", "RelationshipType"),
    ]
