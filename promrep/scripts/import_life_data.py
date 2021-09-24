# -*- coding: utf-8 -*-

# import csv
from os import path

import unicodecsv as csv
from promrep.models import DateInformation, DateType, Person, SecondarySource


def read_input_file(ifname):  # noqa
    file_basename = path.basename(ifname)
    file_basename = path.splitext(file_basename)[0]

    log_fname = file_basename + "_import-log.csv"

    #    sec_source, created = SecondarySource.objects.get_or_create(
    #        name="Nicolet Equites Data", biblio="Nicolet Biblio Entry",
    #        abbrev_name="Nicolet")

    # log file with the ids of the objects created in the database
    csv_log = csv.DictWriter(
        open(log_fname, "wb"),
        ["person_id", "person", "status_assertion", "post_assertion"],
        dialect="excel",
        delimiter=";",
        extrasaction="ignore",
    )
    csv_log.writeheader()

    with open(ifname, "rU") as csvfile:
        csvDict = csv.DictReader(csvfile, delimiter=";")

        for row_dict in csvDict:
            person_id = row_dict["Person ID"]

            # will fail if we don't find the person, mostly for debug purposes
            try:
                person = Person.objects.get(id=person_id)

                # can have up to 5 dates
                for i in range(1, 6):
                    date_str = row_dict["Date{}".format(i)].strip()
                    date_ref = row_dict["DateRef{}".format(i)].strip()
                    uncertain_str = row_dict["DateUncertain{}".format(i)].strip()
                    date_type_str = row_dict["DateType{}".format(i)].strip()
                    date_note = row_dict["DateNotes{}".format(i)].strip()

                    sec_source = False
                    if date_ref:
                        try:
                            sec_source = SecondarySource.objects.get(
                                abbrev_name=date_ref
                            )
                        except:
                            sec_source, created = SecondarySource.objects.get_or_create(
                                abbrev_name=date_ref, biblio=date_ref, name=date_ref
                            )

                    if date_str:
                        # print i, row_dict

                        unc_flag = False
                        if uncertain_str:
                            unc_flag = True

                        date_type, created = DateType.objects.get_or_create(
                            name=date_type_str
                        )

                        # date can be in intervals;
                        # if we have a before or after,
                        #    we'll only create a single point
                        interval = "S"

                        if "before" in date_str:
                            # B: Before
                            interval = "B"
                            date_str = date_str.replace("before", "").strip()
                            date_str = -int(date_str)
                        elif "after" in date_str:
                            # A: After
                            interval = "A"
                            date_str = date_str.replace("after", "").strip()
                            date_str = -int(date_str)
                        elif "by" in date_str:
                            # B: Before
                            interval = "B"
                            date_str = date_str.replace("by", "").strip()
                            date_str = -int(date_str) - 1
                        elif "AD" in date_str:
                            date_str = date_str.replace("AD", "").strip()
                            date_str = int(date_str)
                        else:
                            date_str = -int(date_str)

                        try:
                            di = DateInformation.objects.create(
                                person_id=person.id,
                                value=date_str,
                                uncertain=unc_flag,
                                date_type=date_type,
                                notes=date_note,
                                date_interval=interval,
                            )

                            if sec_source:
                                di.secondary_source = sec_source
                                di.save()

                        except:
                            print(
                                (
                                    "Cannot create DateInformation object".format(
                                        row_dict
                                    )
                                )
                            )

                        print(("Added {} to Person {}".format(di.id, person.id)))

            except Exception as e:
                print(e)
                print(("Cannot find person with id={}".format(person_id)))

    print(('Wrote log file "{}"'.format(log_fname)))


def run():
    ifname = "promrep/scripts/data/life_data/LifeDatesV4.csv"

    print(('Importing data from "{}"'.format(ifname)))
    read_input_file(ifname)
