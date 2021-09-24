# -*- coding: utf-8 -*-

import csv
from os import path

from promrep.models import Person

ICSV_COLUMNS = ["person_id", "nobilis", "nobilis_notes"]


def read_input_file(ifname):  # noqa

    file_basename = path.basename(ifname)
    file_basename = path.splitext(file_basename)[0]

    with open(ifname, "rU") as csvfile:

        csvDict = csv.DictReader(
            csvfile,
            fieldnames=ICSV_COLUMNS,
        )

        # skips first row
        next(csvDict)

        for row_dict in csvDict:
            person_id = int(row_dict["person_id"])
            print(person_id)

            person = Person.objects.get(id=person_id)

            nobilis_str = row_dict["nobilis"].strip()
            nobilis_notes = row_dict["nobilis_notes"].strip()

            if nobilis_str == "Yes":
                person.nobilis = True
                person.nobilis_notes = nobilis_notes.strip()
                person.save()
            else:
                print("Unexpected flag: {}".format(nobilis_str))


def run():
    ifname = "promrep/scripts/data/nobilesV2.csv"

    print(('Importing data from "{}"'.format(ifname)))
    read_input_file(ifname)
