# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promrep', '0020_rename_relation_relationshiptype'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationshipAssertion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('relationship_number', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('uncertain', models.BooleanField(default=False, verbose_name=b'Uncertain')),
                ('original_text', models.CharField(max_length=1024, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('review_flag', models.BooleanField(default=False, verbose_name=b'Review needed')),
                ('created_by', models.ForeignKey(related_name='relationshipassertion_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('inverse_relationship', models.ForeignKey(blank=True, to='promrep.RelationshipAssertion', null=True)),
                ('person', models.ForeignKey(related_name='relationships_as_subject', to='promrep.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelationshipAssertionPrimarySource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('original_text', models.CharField(max_length=1024, blank=True)),
                ('created_by', models.ForeignKey(related_name='relationshipassertionprimarysource_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('primary_source', models.ForeignKey(to='promrep.PrimarySource')),
                ('relationship_assertion', models.ForeignKey(to='promrep.RelationshipAssertion')),
                ('updated_by', models.ForeignKey(related_name='relationshipassertionprimarysource_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='relationshipassertion',
            name='primary_source',
            field=models.ManyToManyField(to='promrep.PrimarySource', null=True, through='promrep.RelationshipAssertionPrimarySource', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relationshipassertion',
            name='related_person',
            field=models.ForeignKey(related_name='relationships_as_object', to='promrep.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relationshipassertion',
            name='related_relationship',
            field=models.ForeignKey(related_name='next', blank=True, to='promrep.RelationshipAssertion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relationshipassertion',
            name='relationship',
            field=models.ForeignKey(to='promrep.RelationshipType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relationshipassertion',
            name='secondary_source',
            field=models.ForeignKey(to='promrep.SecondarySource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relationshipassertion',
            name='updated_by',
            field=models.ForeignKey(related_name='relationshipassertion_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='relationshiptype',
            name='created_by',
            field=models.ForeignKey(related_name='relationshiptype_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='relationshiptype',
            name='updated_by',
            field=models.ForeignKey(related_name='relationshiptype_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
