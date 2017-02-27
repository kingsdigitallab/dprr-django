from __future__ import unicode_literals

import re

from django.db import migrations


def populate_dprr_id(apps, schema_editor):
    Person = apps.get_model('promrep', 'Person')

    for p in Person.objects.all():
        p.dprr_id = generate_dprr_id(p)
        p.save()


def generate_dprr_id(person):
    if not person.nomen:
        return None

    nomen = person.nomen.upper()

    if nomen[0] == '-':
        nomen = 'ANON'

    if '(' in nomen:
        nomen = re.sub(r'\W', '', nomen)

    return '{}{:0>4}'.format(nomen[:4], person.id)


def delete_dprr_id(apps, schema_editor):
    Person = apps.get_model('promrep', 'Person')

    for p in Person.objects.all():
        p.dprr_id = None
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0062_after_pip_packages_upgrade'),
    ]

    operations = [
        migrations.RunPython(populate_dprr_id, reverse_code=delete_dprr_id),
    ]
