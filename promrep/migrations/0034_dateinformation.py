# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promrep', '0033_auto_20160126_1023'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('date_interval', models.CharField(default=b'A', max_length=1, verbose_name=b'Interval', choices=[(b'A', b'Attestation'), (b'F', b'First'), (b'L', b'Last')])),
                ('uncertain', models.BooleanField(default=False)),
                ('value', models.IntegerField()),
                ('source_text', models.TextField()),
                ('notes', models.TextField()),
                ('created_by', models.ForeignKey(related_name='dateinformation_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('date_type', models.ForeignKey(related_name='person_date', verbose_name=b'Type', to='promrep.DateType')),
                ('person', models.ForeignKey(to='promrep.Person')),
                ('secondary_source', models.ForeignKey(blank=True, to='promrep.SecondarySource', null=True)),
                ('updated_by', models.ForeignKey(related_name='dateinformation_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Date',
            },
        ),
    ]
