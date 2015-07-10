# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

def copy_old_locations_to_new(apps, schema_editor):
    """Adds the old locations as new locations"""
    postassertion_model = apps.get_model('promrep', 'PostAssertion')
    postlocation_model = apps.get_model('promrep', 'PostLocation')

    for pa in postassertion_model.objects.all():
        if pa.old_location:
            location = pa.old_location
            pal = postlocation_model(post_assertion = pa, location = location)
            pal.save()
        else:
            pass

def revert_locations_to_old(apps, schema_editor):
    """Moves the new locations to the old_location column"""
    postassertion_model = apps.get_model('promrep', 'PostAssertion')

    for pa in postassertion_model.objects.all():
        if pa.locations:
            # we can safely assume only the first element needs to be copied
            location = pa.locations.first()
            if not pa.old_location:
                pa.old_location = location
                pa.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promrep', '0003_alter_field_post_assertion__old_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uncertain', models.BooleanField(default=False, verbose_name=b'Uncertain')),
                ('note', models.CharField(max_length=1024, blank=True)),
                ('created_by', models.ForeignKey(related_name='postlocation_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('location', models.ForeignKey(to='promrep.Location')),
                ('post_assertion', models.ForeignKey(to='promrep.PostAssertion')),
                ('updated_by', models.ForeignKey(related_name='postlocation_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='postassertion',
            name='location_note',
            field=models.CharField(max_length=1024, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postassertion',
            name='location_original',
            field=models.CharField(max_length=1024, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postassertion',
            name='locations',
            field=models.ManyToManyField(to='promrep.Location', null=True, through='promrep.PostLocation', blank=True),
            preserve_default=True,
        ),

        migrations.RunPython(copy_old_locations_to_new, reverse_code=revert_locations_to_old),
    ]
