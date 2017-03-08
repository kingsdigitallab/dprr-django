from __future__ import unicode_literals

from django.db import migrations

STATUS_TYPE = [('Eques', 'eq. R.'), ('senator', 'sen.')]


def populate_abbrev_name(apps, schema_editor):
    StatusType = apps.get_model('promrep', 'StatusType')

    for item in STATUS_TYPE:
        st, _ = StatusType.objects.get_or_create(name=item[0])
        st.abbrev_name = item[1]
        st.save()


def delete_abbrev_name(apps, schema_editor):
    StatusType = apps.get_model('promrep', 'StatusType')

    for st in StatusType.objects.all():
        st.abbrev_name = None
        st.save()


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0070_statustype_abbrev_name'),
    ]

    operations = [
        migrations.RunPython(
            populate_abbrev_name, reverse_code=delete_abbrev_name),
    ]
