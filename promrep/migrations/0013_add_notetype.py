# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


def load_data(apps, schema_editor):
    note_type_model = apps.get_model("promrep", "NoteType")

    note_type_model(name="Reference Note").save()
    note_type_model(name="Footnote").save()
    note_type_model(name="Reference Note (Office)").save()
    note_type_model(name="Footnote (Office)").save()


class Migration(migrations.Migration):

    dependencies = [
        ('promrep', '0012_auto_20150914_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteType',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(
                    default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(
                    default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('description', models.TextField(max_length=1024, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(load_data),
    ]
