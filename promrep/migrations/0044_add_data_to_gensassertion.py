from __future__ import unicode_literals

from django.db import migrations


def populate_gens_assertions(apps, schema_editor):
    """Populates the new GensAssertion model from the data currently in the
    Person model."""
    Person = apps.get_model('promrep', 'Person')
    GensAssertion = apps.get_model('promrep', 'GensAssertion')

    for p in Person.objects.all():
        if p.gens:
            ga = GensAssertion()
            ga.person = p
            ga.gens = p.gens
            ga.uncertain = p.gens_uncertain
            ga.save()


def delete_gens_assertions(apps, schema_editor):
    """Deletes all the date in the GensAssertion model."""
    GensAssertion = apps.get_model('promrep', 'GensAssertion')
    GensAssertion.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0043_add_model_gensassertion'),
    ]

    operations = [
        migrations.RunPython(
            populate_gens_assertions, reverse_code=delete_gens_assertions),
    ]
