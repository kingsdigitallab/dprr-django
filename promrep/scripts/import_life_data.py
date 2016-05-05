# -*- coding: utf-8 -*-

# import csv
import unicodecsv as csv
import itertools
from os import path
import primary_source_aux as psource_aux

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
            date_notes = row_dict['Notes']

            # will fail if we don't find the person, mostly for debug purposes
            person = Person.objects.get(id=person_id)

            # can have up to 5 dates
            for i in range(1, 5):
                date_str = row_dict['Date{}'.format(i)].strip()
                date_ref = row_dict['DateRef{}'.format(i)].strip()
                uncertain_str = row_dict['DateUncertain{}'.format(i)].strip()
                date_type_str = row_dict['DateType{}'.format(i)]

                if date_str or date_ref:
                    # print i, row_dict

                    unc_flag = False
                    if uncertain_str:
                        unc_flag = True

                    date_type, created = DateType.objects.get_or_create(
                        name=date_type_str)

                    # naive way of adding the sources
                    sec_source, created = SecondarySource.objects.get_or_create(
                        abbrev_name=date_ref,
                        biblio=date_ref,
                        name=date_ref)

                    # date can be in intervals;
                    # if we have a before or after, we'll only create a single
                    # point
                    interval = "Single"

                    if "before" in date_str:
                        interval = "Before"
                        date_str = date_str.replace('before', '').strip()
                    elif "after" in date_str:
                        interval = "After"
                        date_str = date_str.replace('after', '').strip()

                    di = DateInformation.objects.create(
                        person_id=person.id,
                        value=date_str,
                        uncertain=unc_flag,
                        date_type=date_type,
                        secondary_source=sec_source
                    )

                    print("Added {} to Person {}".format(di.id, person.id))

    print("Wrote log file \"{}\"".format(log_fname))


def run():
    ifname = "promrep/scripts/data/life_data/SampleFileForLF13Apr.csv"

    print("Importing data from \"{}\"".format(ifname))
    read_input_file(ifname)
