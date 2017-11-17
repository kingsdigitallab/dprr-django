# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.core.exceptions import ObjectDoesNotExist

def add_type(apps,name):
    RelationshipType=apps.get_model("promrep", "RelationshipType")
    try:
        RelationshipType.objects.get(name=name)
    except ObjectDoesNotExist:
        RelationshipType(name=name, description=name).save()

#Add some missing relationship types so that inverse function works properly
def add_relationship_types(apps,schema_editor):
    add_type(apps,"adoptive mother of")
    add_type(apps,"aunt of")
    add_type(apps,"niece of")
    add_type(apps,"adoptive sister of")
    add_type(apps,"stepdaughter of")
    add_type(apps,"adopted daughter of")
    add_type(apps,"stepmother of")
    add_type(apps,"stepsister of")
    add_type(apps,"great granddaughter of")
    add_type(apps,"great nephew of")
    add_type(apps,"great niece of")
    add_type(apps,"adopted grandmother of")
    add_type(apps,"adopted grandfather of")
    add_type(apps,"great grandmother of")



class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0056_statusassertion_is_verified'),
    ]

    operations = [
        migrations.RunPython(add_relationship_types)
    ]
