import os

import unicodecsv as csv
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from promrep.models import Person


class Command(BaseCommand):
    help = 'Imports life dates into the Persons from the CSV file in data'

    def handle(self, *args, **options):
        try:
            file_name = 'data/era_dates.csv'
            file_path = os.path.abspath(file_name)

            csv_file = open(file_path)
            csv_dict = csv.DictReader(csv_file)

            for row in csv_dict:
                person_id = row['person_id']
                era_from = self._get_int_from_str(row['era_from'])
                era_to = self._get_int_from_str(row['era_to'])

                self._set_person_era(person_id, era_from, era_to)
        except IOError:
            raise CommandError('Era dates file not found: {}'.format(
                file_name
            ))

    def _get_int_from_str(self, value):
        try:
            return int(value)
        except ValueError:
            return None

    def _set_person_era(self, person_id, era_from, era_to):
        try:
            person = Person.objects.get(id=person_id)

            if era_from:
                person.era_from = era_from

            if era_to:
                person.era_to = era_to

            person.save()
        except ObjectDoesNotExist:
            self.stderr.write('Person with ID {} not found.'.format(person_id))
