# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        from django.core.management import call_command

        call_command("loaddata", "promrep/fixtures/promrep_sex.json")
        call_command("loaddata", "promrep/fixtures/promrep_praenomina.json")

    def backwards(self, orm):
        "Write your backwards methods here."

        pass


    complete_apps = ['promrep']
    symmetrical = True
