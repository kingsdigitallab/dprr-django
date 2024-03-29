# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 11:48


from django.db import migrations
from django.db.models import Q


def remove_relationshiptype(apps, id_to_copy, id_to_delete):
    RelationshipType = apps.get_model("promrep", "RelationshipType")
    RelationshipAssertion = apps.get_model("promrep", "RelationshipAssertion")
    RelationshipInverse = apps.get_model("promrep", "RelationshipInverse")
    type_to_copy = RelationshipType.objects.get_or_create(name=id_to_copy)[0]
    type_to_delete = RelationshipType.objects.get_or_create(name=id_to_delete)[0]
    # Check for assertions, eset existing as type
    for assertion in RelationshipAssertion.objects.filter(relationship=type_to_delete):
        assertion.relationship = type_to_copy
        assertion.save()
    for inverse in RelationshipInverse.objects.filter(
        Q(relationship=type_to_delete) | Q(inverse_relationship=type_to_delete)
    ):
        inverse.delete()
    type_to_delete.delete()


def remove_duplicates(apps, schema_editor):
    remove_relationshiptype(apps, "adoptive grandfather", "adopted grandfather")


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0074_remove_duplicate_relationshiptypes"),
    ]

    operations = [migrations.RunPython(remove_duplicates)]
