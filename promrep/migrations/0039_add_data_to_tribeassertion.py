from __future__ import unicode_literals

from django.db import migrations


def populate_tribe_assertions(apps, schema_editor):
    """Populates the new TribeAssertion model from the data currently in the
    Person model."""
    Person = apps.get_model('promrep', 'Person')
    TribeAssertion = apps.get_model('promrep', 'TribeAssertion')

    for p in Person.objects.all():
        if p.tribe:
            ta = TribeAssertion()
            ta.person = p
            ta.tribe = p.tribe
            ta.uncertain = p.tribe_uncertain
            ta.save()


def delete_tribe_assertions(apps, schema_editor):
    """Deletes all the date in the TribeAssertion model."""
    TribeAssertion = apps.get_model('promrep', 'TribeAssertion')
    TribeAssertion.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0038_alter_field_tribeassertion_secondary_source'),
    ]

    operations = [
        migrations.RunPython(
            populate_tribe_assertions, reverse_code=delete_tribe_assertions),
    ]
