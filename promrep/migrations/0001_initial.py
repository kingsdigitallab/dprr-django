# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.utils.timezone
import model_utils.fields
import promrep.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assertion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('display_text', models.CharField(max_length=1024, blank=True)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssertionNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('note_type', models.CharField(max_length=1, choices=[(b'r', b'Reference (Body of text)'), (b'e', b'Endnote (Broughton only)')])),
                ('extra_info', models.CharField(max_length=128, blank=True)),
                ('text', models.CharField(max_length=1024, blank=True)),
            ],
            options={
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
                ('certainty', models.BooleanField(default=True, verbose_name=b'Certainty?')),
                ('assertion', models.ForeignKey(to='promrep.Assertion')),
            ],
            options={
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
            name='Date',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('interval', models.SmallIntegerField(choices=[(0, b'single'), (1, b'min'), (2, b'max')])),
                ('year', promrep.models.IntegerRangeField(null=True, blank=True)),
                ('year_uncertain', models.BooleanField(default=None, verbose_name=b'uncertain')),
                ('circa', models.BooleanField(default=None)),
                ('extra_info', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
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
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='promrep.Office', null=True)),
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
                ('real_attribute', models.CharField(help_text=b'Original RE entry (from source)', max_length=128, verbose_name=b'RE attribute', blank=True)),
                ('patrician', models.BooleanField(default=False, verbose_name=b'Patrician?')),
                ('patrician_certainty', models.BooleanField(default=True, verbose_name=b'Patrician Certainty?')),
                ('extra_info', models.CharField(help_text=b'Extra info about the person.', max_length=1024, blank=True)),
                ('review_flag', models.BooleanField(default=False, help_text=b'Person needs manual revision.', verbose_name=b'Review needed')),
                ('gens', models.ForeignKey(blank=True, to='promrep.Gens', null=True)),
                ('origin', models.ForeignKey(blank=True, to='promrep.Origin', null=True)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('note_type', models.CharField(max_length=1, choices=[(b'r', b'Reference (Body of text)'), (b'e', b'Endnote (Broughton only)')])),
                ('extra_info', models.CharField(max_length=128, blank=True)),
                ('text', models.CharField(max_length=1024, blank=True)),
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
            field=models.ForeignKey(blank=True, to='promrep.Sex', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='tribe',
            field=models.ForeignKey(blank=True, to='promrep.Tribe', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('praenomen', 'nomen', 'real_number')]),
        ),
        migrations.AddField(
            model_name='date',
            name='date_type',
            field=models.ForeignKey(blank=True, to='promrep.DateType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertionperson',
            name='notes',
            field=models.ManyToManyField(to='promrep.PersonNote'),
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
            model_name='assertion',
            name='assertion_type',
            field=models.ForeignKey(to='promrep.AssertionType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertion',
            name='notes',
            field=models.ManyToManyField(to='promrep.AssertionNote'),
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
            name='secondary_source',
            field=models.ForeignKey(to='promrep.SecondarySource'),
            preserve_default=True,
        ),
    ]
