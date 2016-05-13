# -*- coding: utf-8 -*-

# import csv
import unicodecsv as csv
import itertools
from os import path
import primary_source_aux as psource_aux
from django.db import utils

from promrep.models import Person, DateType, DateInformation, SecondarySource


def read_input_file(ifname):
    file_basename = path.basename(ifname)
    file_basename = path.splitext(file_basename)[0]

    log_fname = file_basename + "_import-log.csv"

#    sec_source, created = SecondarySource.objects.get_or_create(
#        name="Nicolet Equites Data", biblio="Nicolet Biblio Entry",
#        abbrev_name="Nicolet")

    # log file with the ids of the objects created in the database
    csv_log = csv.DictWriter(open(log_fname, 'wb'),
                             ["person_id", "person",
                                 "status_assertion", "post_assertion"],
                             dialect='excel',
                             delimiter=";",
                             extrasaction='ignore')
    csv_log.writeheader()

    stats = {'person': {'new': 0, 'old': 0, 'found': 0}}

    with open(ifname, 'rU') as csvfile:
        # fields:
        # Person
        # ID;Date1;DateUncertain1;DateType1;DateRef1;Date2;DateUncertain2;DateType2;DateRef2;Date3;DateUncertain3;DateType3;DateRef3;Date4;DateUncertain4;DateType4;DateRef4;Date5;DateUncertain5;DateType5;DateRef5;Notes;

        csvDict = csv.DictReader(csvfile,
                                 # fieldnames=ICSV_COLUMNS,
                                 delimiter=";")

        for row_dict in csvDict:
            person_id = row_dict['Person ID']

            # will fail if we don't find the person, mostly for debug purposes
            try:
                person = Person.objects.get(id=person_id)

                # can have up to 5 dates
                for i in range(1, 6):
                    date_str = row_dict['Date{}'.format(i)].strip()
                    date_ref = row_dict['DateRef{}'.format(i)].strip()
                    uncertain_str = row_dict['DateUncertain{}'.format(i)].strip()
                    date_type_str = row_dict['DateType{}'.format(i)].strip()
                    date_note = row_dict['DateNotes{}'.format(i)].strip()

                    if date_str:
                        # print i, row_dict

                        unc_flag = False
                        if uncertain_str:
                            unc_flag = True

                        date_type, created = DateType.objects.get_or_create(
                            name=date_type_str)

                        # date can be in intervals;
                        # if we have a before or after, we'll only create a single
                        # point
                        interval = "S"

                        if "before" in date_str:
                            # B: Before
                            interval = "B"
                            date_str = date_str.replace('before', '').strip()
                            date_str = - int(date_str)
                        elif "after" in date_str:
                            # A: After
                            interval = "A"
                            date_str = date_str.replace('after', '').strip()
                            date_str = - int(date_str)
                        elif "by" in date_str:
                            # B: Before
                            interval = "B"
                            date_str = date_str.replace('by', '').strip()
                            date_str = - int(date_str) - 1
                        elif "AD" in date_str:
                            date_str = date_str.replace('AD', '').strip()
                            date_str = int(date_str)
                        else:
                            date_str = - int(date_str)

                        try:
                            di = DateInformation.objects.create(
                                person_id=person.id,
                                value=date_str,
                                uncertain=unc_flag,
                                date_type=date_type,
                                notes = date_note,
                                date_interval = interval
                            )

                            # naive way of adding the sources
                            if date_ref:
                                sec_source, created = SecondarySource.objects.get_or_create(
                                    abbrev_name=date_ref,
                                    biblio=date_ref,
                                    name=date_ref)
                                di.secondary_source = sec_source
                                di.save()

                        except e:
                            print("Cannot create DateInformation object".format(row_dict))

                        print("Added {} to Person {}".format(di.id, person.id))

            except Exception as e:
                print e
                print("Cannot find person with id={}".format(person_id))


    print("Wrote log file \"{}\"".format(log_fname))


def run():
    ifname = "promrep/scripts/data/life_data/LifeDatesV2.csv"

    print("Importing data from \"{}\"".format(ifname))
    read_input_file(ifname)
