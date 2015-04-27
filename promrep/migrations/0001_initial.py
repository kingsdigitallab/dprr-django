# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DateType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('description', models.CharField(max_length=1024, blank=True)),
                ('created_by', models.ForeignKey(related_name='datetype_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='datetype_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gens',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('extra_info', models.CharField(max_length=1024, blank=True)),
                ('created_by', models.ForeignKey(related_name='gens_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='gens_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Gens',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('description', models.CharField(max_length=1024, blank=True)),
                ('location_type', models.SmallIntegerField(default=0, choices=[(0, b'place'), (1, b'province')])),
                ('created_by', models.ForeignKey(related_name='location_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='location_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Places',
                'verbose_name_plural': 'Place List',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('description', models.CharField(max_length=1024, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('created_by', models.ForeignKey(related_name='office_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='promrep.Office', null=True)),
                ('updated_by', models.ForeignKey(related_name='office_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft', 'name'],
                'verbose_name': 'Office List',
                'verbose_name_plural': 'Office List',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Origin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('extra_info', models.CharField(max_length=1024, blank=True)),
                ('created_by', models.ForeignKey(related_name='origin_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='origin_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('praenomen_uncertain', models.BooleanField(default=False, verbose_name=b'Uncertain Praenomen')),
                ('nomen', models.CharField(max_length=128, blank=True)),
                ('nomen_uncertain', models.BooleanField(default=False, verbose_name=b'Uncertain Nomen')),
                ('cognomen', models.CharField(max_length=64, blank=True)),
                ('cognomen_uncertain', models.BooleanField(default=False, verbose_name=b'Uncertain Cognomen')),
                ('other_names', models.CharField(max_length=128, blank=True)),
                ('filiation', models.CharField(max_length=256, blank=True)),
                ('filiation_uncertain', models.BooleanField(default=False, verbose_name=b'Uncertain Filiation')),
                ('gens_uncertain', models.BooleanField(default=False, verbose_name=b'Uncertain Gens')),
                ('tribe_uncertain', models.BooleanField(default=False, verbose_name=b'Uncertain Tribe')),
                ('re_number', models.CharField(help_text=b'RE number', max_length=32, verbose_name=b'RE Number', blank=True)),
                ('re_number_old', models.CharField(help_text=b'RE number before revising', max_length=32, verbose_name=b'RE (old)', blank=True)),
                ('patrician', models.NullBooleanField(default=None, verbose_name=b'Patrician')),
                ('patrician_uncertain', models.BooleanField(default=False, verbose_name=b'Uncertain Patrician')),
                ('patrician_notes', models.TextField(blank=True)),
                ('novus', models.NullBooleanField(default=None)),
                ('novus_uncertain', models.NullBooleanField(default=False)),
                ('novus_notes', models.TextField(blank=True)),
                ('eques', models.NullBooleanField(default=None)),
                ('eques_uncertain', models.BooleanField(default=False)),
                ('eques_notes', models.TextField(blank=True)),
                ('nobilis', models.NullBooleanField(default=None)),
                ('nobilis_uncertain', models.BooleanField(default=False)),
                ('nobilis_notes', models.TextField(blank=True)),
                ('extra_info', models.TextField(help_text=b'Extra info about the person.', blank=True)),
                ('date_first', models.IntegerField(null=True, blank=True)),
                ('date_last', models.IntegerField(null=True, blank=True)),
                ('era_from', models.IntegerField(null=True, blank=True)),
                ('era_to', models.IntegerField(null=True, blank=True)),
                ('review_flag', models.BooleanField(default=False, help_text=b'Person needs manual revision.', verbose_name=b'Review needed')),
                ('created_by', models.ForeignKey(related_name='person_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('date_first_type', models.ForeignKey(related_name='person_first', blank=True, to='promrep.DateType', null=True)),
                ('date_last_type', models.ForeignKey(related_name='person_last', blank=True, to='promrep.DateType', null=True)),
                ('gens', models.ForeignKey(blank=True, to='promrep.Gens', null=True)),
                ('origin', models.ForeignKey(blank=True, to='promrep.Origin', null=True)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('display_text', models.CharField(max_length=1024, blank=True)),
                ('uncertain', models.BooleanField(default=False, verbose_name=b'Uncertain')),
                ('date_year', models.IntegerField(blank=True)),
                ('date_info', models.CharField(max_length=1024, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='post_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('location', models.ForeignKey(blank=True, to='promrep.Location', null=True)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostAssertion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('original_text', models.CharField(max_length=1024, blank=True)),
                ('office_xref', models.CharField(max_length=1024, blank=True)),
                ('uncertain', models.BooleanField(default=False, verbose_name=b'Uncertain')),
                ('position', models.PositiveSmallIntegerField(default=0)),
                ('date_start', models.IntegerField(null=True, blank=True)),
                ('date_start_uncertain', models.BooleanField(default=False)),
                ('date_end', models.IntegerField(null=True, blank=True)),
                ('date_end_uncertain', models.BooleanField(default=False)),
                ('date_info', models.CharField(max_length=1024, null=True, blank=True)),
                ('review_flag', models.BooleanField(default=False, help_text=b'Manual revision needed.', verbose_name=b'Review needed')),
                ('created_by', models.ForeignKey(related_name='postassertion_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['position', 'id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostAssertionNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('note_type', models.IntegerField(default=0, choices=[(0, b'Reference'), (1, b'Footnote'), (2, b'Reference (Office)'), (3, b'Footnote (Office)')])),
                ('text', models.TextField(blank=True)),
                ('extra_info', models.TextField(max_length=1024, blank=True)),
                ('created_by', models.ForeignKey(related_name='postassertionnote_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('note_type', models.IntegerField(default=0, choices=[(0, b'Reference'), (1, b'Footnote'), (2, b'Reference (Office)'), (3, b'Footnote (Office)')])),
                ('text', models.TextField(blank=True)),
                ('extra_info', models.TextField(max_length=1024, blank=True)),
                ('created_by', models.ForeignKey(related_name='postnote_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Praenomen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbrev', models.CharField(unique=True, max_length=32)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('created_by', models.ForeignKey(related_name='praenomen_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='praenomen_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Praenomina',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrimarySource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('description', models.CharField(max_length=1024, blank=True)),
                ('created_by', models.ForeignKey(related_name='relationship_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='relationship_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoleType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('description', models.CharField(max_length=1024, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SecondarySource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('abbrev_name', models.CharField(unique=True, max_length=256, blank=True)),
                ('biblio', models.CharField(unique=True, max_length=512, blank=True)),
                ('created_by', models.ForeignKey(related_name='secondarysource_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='secondarysource_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tribe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbrev', models.CharField(unique=True, max_length=32)),
                ('name', models.CharField(max_length=128)),
                ('extra_info', models.CharField(max_length=1024, blank=True)),
                ('created_by', models.ForeignKey(related_name='tribe_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='tribe_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='postnote',
            name='secondary_source',
            field=models.ForeignKey(to='promrep.SecondarySource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postnote',
            name='updated_by',
            field=models.ForeignKey(related_name='postnote_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postassertionnote',
            name='secondary_source',
            field=models.ForeignKey(to='promrep.SecondarySource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postassertionnote',
            name='updated_by',
            field=models.ForeignKey(related_name='postassertionnote_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postassertion',
            name='notes',
            field=models.ManyToManyField(to='promrep.PostAssertionNote', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postassertion',
            name='person',
            field=models.ForeignKey(to='promrep.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postassertion',
            name='post',
            field=models.ForeignKey(to='promrep.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postassertion',
            name='role',
            field=models.ForeignKey(default=1, to='promrep.RoleType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postassertion',
            name='secondary_source',
            field=models.ForeignKey(to='promrep.SecondarySource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postassertion',
            name='updated_by',
            field=models.ForeignKey(related_name='postassertion_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='notes',
            field=models.ManyToManyField(related_name='posts', to='promrep.PostNote', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='office',
            field=models.ForeignKey(blank=True, to='promrep.Office', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='persons',
            field=models.ManyToManyField(to='promrep.Person', through='promrep.PostAssertion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='updated_by',
            field=models.ForeignKey(related_name='post_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='praenomen',
            field=models.ForeignKey(blank=True, to='promrep.Praenomen', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='sex',
            field=models.ForeignKey(default=1, blank=True, to='promrep.Sex', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='tribe',
            field=models.ForeignKey(blank=True, to='promrep.Tribe', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='updated_by',
            field=models.ForeignKey(related_name='person_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
