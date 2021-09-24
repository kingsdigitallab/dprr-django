from django.db import migrations


def populate_dprr_id(apps, schema_editor):
    Person = apps.get_model("promrep", "Person")

    for p in Person.objects.all():
        p.dprr_id = generate_dprr_id(p)
        p.save()


def generate_dprr_id(person):
    if not person.nomen:
        return None

    return "{}{:0>4}".format(person.nomen.upper()[:4], person.id)


def delete_dprr_id(apps, schema_editor):
    Person = apps.get_model("promrep", "Person")

    for p in Person.objects.all():
        p.dprr_id = None
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ("promrep", "0060_person_dprr_id"),
    ]

    operations = [
        migrations.RunPython(populate_dprr_id, reverse_code=delete_dprr_id),
    ]
