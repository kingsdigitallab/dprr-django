# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

def copy_old_locations_to_new(apps, schema_editor):
    """Adds the old locations as new locations"""
    postassertion_model = apps.get_model('promrep', 'PostAssertion')
    postassertinoprovince_model = apps.get_model('promrep', 'PostAssertionProvince')

    for pa in postassertion_model.objects.all():
        if pa.old_location:
            province = pa.old_location
            pal = postassertinoprovince_model(post_assertion = pa, province = province)
            pal.save()
        else:
            pass

def revert_locations_to_old(apps, schema_editor):
    """Moves the new locations to the old_location column"""
    postassertion_model = apps.get_model('promrep', 'PostAssertion')

    for pa in postassertion_model.objects.all():
        if pa.provinces:
            # we can safely assume only the first element needs to be copied
            province = pa.provinces.first()
            if not pa.old_location:
                pa.old_location = province
                pa.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promrep', '0004_rename_location_province'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostAssertionProvince',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uncertain', models.BooleanField(default=False, verbose_name=b'Uncertain')),
                ('note', models.CharField(max_length=1024, blank=True)),
                ('created_by', models.ForeignKey(related_name='postassertionprovince_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('province', models.ForeignKey(to='promrep.Province')),
                ('post_assertion', models.ForeignKey(to='promrep.PostAssertion')),
                ('updated_by', models.ForeignKey(related_name='postassertionprovince_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='postassertion',
            name='province_original_expanded',
            field=models.CharField(max_length=512, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postassertion',
            name='province_original',
            field=models.CharField(max_length=512, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postassertion',
            name='provinces',
            field=models.ManyToManyField(to='promrep.Province', null=True, through='promrep.PostAssertionProvince', blank=True),
            preserve_default=True,
        ),

        migrations.RunPython(copy_old_locations_to_new, reverse_code=revert_locations_to_old),
    ]