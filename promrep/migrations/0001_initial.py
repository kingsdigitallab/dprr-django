# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.utils.timezone
from django.conf import settings
import model_utils.fields
import promrep.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assertion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('display_text', models.CharField(max_length=1024, blank=True)),
                ('certainty', models.BooleanField(default=True, verbose_name=b'Certainty?')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssertionDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interval', models.SmallIntegerField(default=0, choices=[(0, b'single'), (1, b'min'), (2, b'max')])),
                ('year', promrep.models.IntegerRangeField(blank=True)),
                ('year_uncertain', models.BooleanField(default=False, verbose_name=b'uncertain')),
                ('circa', models.BooleanField(default=False)),
                ('extra_info', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('assertion', models.ForeignKey(related_query_name=b'date', related_name='dates', blank=True, to='promrep.Assertion', null=True)),
                ('created_by', models.ForeignKey(related_name='assertiondate_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssertionNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('note_type', models.IntegerField(default=0, choices=[(0, b'Reference'), (1, b'Footnote')])),
                ('text', models.TextField(blank=True)),
                ('extra_info', models.TextField(max_length=1024, blank=True)),
                ('created_by', models.ForeignKey(related_name='assertionnote_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssertionPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('original_text', models.CharField(max_length=1024, blank=True)),
                ('office_xref', models.CharField(max_length=1024, blank=True)),
                ('certainty', models.BooleanField(default=True, verbose_name=b'Certainty?')),
                ('position', models.PositiveSmallIntegerField(default=0)),
                ('assertion', models.ForeignKey(to='promrep.Assertion')),
                ('created_by', models.ForeignKey(related_name='assertionperson_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['position', 'id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssertionPersonDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interval', models.SmallIntegerField(default=0, choices=[(0, b'single'), (1, b'min'), (2, b'max')])),
                ('year', promrep.models.IntegerRangeField(blank=True)),
                ('year_uncertain', models.BooleanField(default=False, verbose_name=b'uncertain')),
                ('circa', models.BooleanField(default=False)),
                ('extra_info', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('assertion_person', models.ForeignKey(related_query_name=b'date', related_name='dates', blank=True, to='promrep.AssertionPerson', null=True)),
                ('created_by', models.ForeignKey(related_name='assertionpersondate_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssertionPersonNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('note_type', models.IntegerField(default=0, choices=[(0, b'Reference'), (1, b'Footnote')])),
                ('text', models.TextField(blank=True)),
                ('extra_info', models.TextField(max_length=1024, blank=True)),
                ('created_by', models.ForeignKey(related_name='assertionpersonnote_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssertionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DateType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True)),
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
                'verbose_name_plural': 'Offices',
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
                ('praenomen_certainty', models.BooleanField(default=True, verbose_name=b'Praenomen Certainty?')),
                ('nomen', models.CharField(max_length=128, blank=True)),
                ('cognomen', models.CharField(max_length=64, blank=True)),
                ('other_names', models.CharField(max_length=128, blank=True)),
                ('filiation', models.CharField(max_length=256, blank=True)),
                ('real_number', models.CharField(help_text=b'RE number', max_length=32, verbose_name=b'RE Number', blank=True)),
                ('real_number_old', models.CharField(help_text=b'RE number before revising', max_length=32, verbose_name=b'RE (old)', blank=True)),
                ('patrician', models.BooleanField(default=False, verbose_name=b'Patrician')),
                ('patrician_certainty', models.BooleanField(default=True, verbose_name=b'Certain')),
                ('extra_info', models.CharField(help_text=b'Extra info about the person.', max_length=1024, blank=True)),
                ('review_flag', models.BooleanField(default=False, help_text=b'Person needs manual revision.', verbose_name=b'Review needed')),
                ('created_by', models.ForeignKey(related_name='person_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('gens', models.ForeignKey(blank=True, to='promrep.Gens', null=True)),
                ('origin', models.ForeignKey(blank=True, to='promrep.Origin', null=True)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interval', models.SmallIntegerField(default=0, choices=[(0, b'single'), (1, b'min'), (2, b'max')])),
                ('year', promrep.models.IntegerRangeField(blank=True)),
                ('year_uncertain', models.BooleanField(default=False, verbose_name=b'uncertain')),
                ('circa', models.BooleanField(default=False)),
                ('extra_info', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('created_by', models.ForeignKey(related_name='persondate_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('date_type', models.ForeignKey(blank=True, to='promrep.DateType', null=True)),
                ('person', models.ForeignKey(related_query_name=b'date', related_name='dates', blank=True, to='promrep.Person', null=True)),
                ('updated_by', models.ForeignKey(related_name='persondate_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
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
        migrations.AddField(
            model_name='assertionpersonnote',
            name='secondary_source',
            field=models.ForeignKey(to='promrep.SecondarySource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertionpersonnote',
            name='updated_by',
            field=models.ForeignKey(related_name='assertionpersonnote_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertionpersondate',
            name='date_type',
            field=models.ForeignKey(blank=True, to='promrep.DateType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertionpersondate',
            name='updated_by',
            field=models.ForeignKey(related_name='assertionpersondate_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertionperson',
            name='notes',
            field=models.ManyToManyField(to='promrep.AssertionPersonNote'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertionperson',
            name='person',
            field=models.ForeignKey(to='promrep.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertionperson',
            name='role',
            field=models.ForeignKey(to='promrep.RoleType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertionperson',
            name='secondary_source',
            field=models.ForeignKey(to='promrep.SecondarySource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertionperson',
            name='updated_by',
            field=models.ForeignKey(related_name='assertionperson_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertionnote',
            name='secondary_source',
            field=models.ForeignKey(to='promrep.SecondarySource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertionnote',
            name='updated_by',
            field=models.ForeignKey(related_name='assertionnote_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertiondate',
            name='date_type',
            field=models.ForeignKey(blank=True, to='promrep.DateType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertiondate',
            name='updated_by',
            field=models.ForeignKey(related_name='assertiondate_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertion',
            name='assertion_type',
            field=models.ForeignKey(to='promrep.AssertionType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertion',
            name='created_by',
            field=models.ForeignKey(related_name='assertion_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertion',
            name='notes',
            field=models.ManyToManyField(related_name='assertions', to='promrep.AssertionNote'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertion',
            name='office',
            field=models.ForeignKey(blank=True, to='promrep.Office', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertion',
            name='persons',
            field=models.ManyToManyField(to='promrep.Person', through='promrep.AssertionPerson'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertion',
            name='relationship',
            field=models.ForeignKey(blank=True, to='promrep.Relationship', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertion',
            name='updated_by',
            field=models.ForeignKey(related_name='assertion_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='AssertionNoteThrough',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('promrep.assertion_notes',),
        ),
    ]
