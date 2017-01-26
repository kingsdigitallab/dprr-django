# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models



class Migration(migrations.Migration):
    dependencies = [
        ('promrep', '0057_add_relationship_types'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationshipInverse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inverse_relationship', models.ForeignKey(related_name='inverse', to='promrep.RelationshipType')),
                ('relationship', models.ForeignKey(to='promrep.RelationshipType')),
                ('sex', models.ForeignKey(to='promrep.Sex')),
            ],
        )

    ]
