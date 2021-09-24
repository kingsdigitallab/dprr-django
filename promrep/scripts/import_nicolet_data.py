# -*- coding: utf-8 -*-

import logging
import pprint
import re
from os import path

import unicodecsv as csv
from promrep.models import (Office, Person, PostAssertion, PostAssertionNote,
                            Praenomen, SecondarySource, Sex, StatusAssertion,
                            StatusAssertionNote, StatusType, Tribe,
                            TribeAssertion)

pp = pprint.PrettyPrinter(width=1)

# Setup logging
LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
LOGGER.setLevel(logging.INFO)

ch = logging.StreamHandler()
log_formatter = logging.Formatter("%(levelname)s: [%(asctime)s] %(message)s")

ch.setFormatter(log_formatter)
LOGGER.addHandler(ch)

ICSV_COLUMNS = [
    "person",
    "post",
    "date_source_text",
    "date_start",
    "date_start_uncertain",
    "date_start_type",
    "date_end",
    "date_end_uncertain",
    "date_end_type",
    "office_name",
    "office_uncertain",
    "praenomen",
    "nomen",
    "RE",
    "filiation",
    "cognomen",
    "other_names",
    "original_text",
    "review_flag",
    "tribe",
    "tribe_uncertain",
    "origin",
    "origin_uncertain",
    "eques",
    "eques_uncertain",
    "notes",
]


def clean_field(field, a_string):
    """cleans uncertain chars from a string, outputs a dictionary
    with the cleaned string and uncertainty flag
    """

    # chars to be removed from  most name fields
    unc_chars = "?[]"
    uncertain = False

    for ch in unc_chars:
        if ch in a_string:
            uncertain = True
            a_string = a_string.replace(ch, "")

    dict_obj = {
        field: a_string,
    }

    if uncertain:
        dict_obj.update({field + "_uncertain": uncertain})

    return dict_obj


def create_person(row_dict):
    """Creates a new person object from a dictionary,
    and returns the new person id
    """

    person_dict = {}
    person_dict["sex"] = Sex.objects.get(name="Male")

    if "sex" in row_dict and row_dict["sex"].strip() == "F":
        person_dict["sex"] = Sex.objects.get(name="Female")

    # praenomen special case
    # we initially clean the string, and then add the object to the dictionary
    praenomen_str = row_dict.get("praenomen")
    if praenomen_str:
        if "." not in praenomen_str:
            praenomen_str = praenomen_str + "."

    praenomen_dic = clean_field("praenomen", praenomen_str)

    try:
        praenomen = Praenomen.objects.get(abbrev=praenomen_dic["praenomen"])
    except Praenomen.DoesNotExist:
        praenomen = Praenomen.objects.get(abbrev="-.")

    praenomen_dic["praenomen"] = praenomen

    # add praenomen info to person object
    person_dict.update(praenomen_dic)

    # cleans the remining person name fields
    for field in ["nomen", "cognomen", "other_names"]:
        field_string = row_dict.get(field)

        if field_string:
            d_obj = clean_field(field, field_string)
            # updates the person dictionary
            person_dict.update(d_obj)

    # remaining person fields, where names were not standard
    person_dict["re_number"] = row_dict.get("re")

    # logger.info(person_dict)
    person, created = Person.objects.get_or_create(**person_dict)

    if created:
        LOGGER.info("Created person with id={}".format(person.id))

    return person.id, created


def read_input_file(ifname):  # noqa

    file_basename = path.basename(ifname)
    file_basename = path.splitext(file_basename)[0]

    log_fname = file_basename + "_import-log.csv"

    sec_source, created = SecondarySource.objects.get_or_create(
        name="Nicolet Equites Data",
        biblio="Nicolet Biblio Entry",
        abbrev_name="Nicolet",
    )

    # log file with the ids of the objects created in the database
    csv_log = csv.DictWriter(
        open(log_fname, "wb"),
        ["person_id", "person", "status_assertion", "post_assertion"],
        dialect="excel",
        delimiter=";",
        extrasaction="ignore",
    )
    csv_log.writeheader()

    stats = {"person": {"new": 0, "old": 0, "found": 0}}

    with open(ifname, "rU") as csvfile:

        csvDict = csv.DictReader(csvfile, fieldnames=ICSV_COLUMNS, delimiter=";")

        # skips header row
        next(csvDict)

        for row_dict in csvDict:

            person_id = int(row_dict["person"])

            if not person_id:
                person_dict = {
                    "praenomen": row_dict["praenomen"],
                    "nomen": row_dict["nomen"],
                    "re": row_dict["RE"],
                    "filiation": row_dict["filiation"],
                    "cognomen": row_dict["cognomen"],
                    "other_names": row_dict["other_names"],
                    "review_flag": row_dict["review_flag"],
                }

                person_id, created = create_person(person_dict)
                if created:
                    stats["person"]["new"] += 1
                    LOGGER.info("Added Person: id={}".format(person_id))
                else:
                    stats["person"]["found"] += 1
                    LOGGER.info("Found Person: id={}".format(person_id))

            else:
                stats["person"]["old"] += 1
                LOGGER.info("Lotus Person: id={}".format(person_id))

            person = Person.objects.get(id=person_id)

            if row_dict["origin"]:
                origin_str = row_dict["origin"]

                if row_dict["origin_uncertain"]:
                    origin_str = origin_str + "?"

                if person.origin:
                    LOGGER.info("Person already had previous Origin info!!!!")
                else:
                    person.origin = origin_str
                    person.save()

            # add the tribe info
            if row_dict["tribe"]:
                for tribe in row_dict["tribe"].split(" or "):
                    tribe_str = tribe.strip()

                    if tribe_str:
                        tribes = Tribe.objects.filter(name__iexact=tribe_str)

                        if tribes.count() == 0:
                            tribe_obj = Tribe.objects.create(
                                name=tribe_str, abbrev=tribe_str
                            )
                        else:
                            tribe_obj = tribes.first()

                        tribe_uncertain = row_dict["tribe_uncertain"]

                        # only created if doesn't exist already
                        if tribe_obj not in person.tribes.all():
                            tr_assert, cr = TribeAssertion.objects.get_or_create(
                                person=person,
                                tribe=tribe_obj,
                                uncertain=tribe_uncertain,
                                secondary_source=sec_source,
                            )

            st_type, created = StatusType.objects.get_or_create(name="Eques")

            st_assert, sa_created = StatusAssertion.objects.get_or_create(
                person=person,
                secondary_source=sec_source,
                uncertain=row_dict["eques_uncertain"],
                status=st_type,
                review_flag=row_dict["review_flag"],
                original_text=row_dict["original_text"],
            )

            if sa_created:
                sa_note = StatusAssertionNote(
                    secondary_source=sec_source,
                    text=row_dict["notes"],
                )
                sa_note.save()
                st_assert.notes.add(sa_note)

            # Dates, post assertions

            date_start_type = row_dict["date_start_type"].strip()
            date_end_type = row_dict["date_end_type"].strip()
            date_start = row_dict["date_start"].strip()
            date_end = row_dict["date_end"].strip()
            date_source_text = row_dict["date_source_text"].strip()

            date_start_uncertain = True
            if row_dict["date_start_uncertain"].strip() == "0":
                date_start_uncertain = False

            date_end_uncertain = True
            if row_dict["date_end_uncertain"].strip() == "0":
                date_end_uncertain = False

            # creates a PostAssertion
            if (date_start_type or date_end_type) == "Office":
                if row_dict["post"].strip() == "0":
                    office_name = row_dict["office_name"].strip()
                    office_list = Office.objects.filter(name__iexact=office_name)

                    if len(office_list):
                        office = Office.objects.get(name__iexact=office_name)
                    else:
                        office, created = Office.objects.get_or_create(name=office_name)

                    pa_assertion, created = PostAssertion.objects.get_or_create(
                        person=person,
                        office=office,
                        secondary_source=sec_source,
                        date_source_text=date_source_text,
                        uncertain=row_dict["office_uncertain"],
                        original_text=row_dict["original_text"],
                        review_flag=row_dict["review_flag"],
                    )

                    if date_start:
                        pa_assertion.date_start = date_start
                    if date_end:
                        pa_assertion.date_end = date_end

                    pa_assertion.date_source_text = date_source_text
                    pa_assertion.date_start_uncertain = date_start_uncertain
                    pa_assertion.date_end_uncertain = date_end_uncertain

                    # in the case of the post assertions, we can ignore the
                    #   text after Nicolet Ref. XYZ.
                    print(row_dict["notes"])
                    pa_txt = re.sub(
                        r"(Nicolet\sRef\s[0-9]+\.).*", r"\1", row_dict["notes"]
                    )
                    print(pa_txt)

                    # adds the note to the post assertion
                    pa_note = PostAssertionNote.objects.create(
                        secondary_source=sec_source,
                        text=pa_txt,
                    )

                    pa_assertion.notes.add(pa_note)
                    pa_assertion.save()

            else:
                if date_start:
                    st_assert.date_start = date_start
                if date_end:
                    st_assert.date_end = date_end

                st_assert.date_source_text = date_source_text
                st_assert.date_start_uncertain = date_start_uncertain
                st_assert.date_end_uncertain = date_end_uncertain

                st_assert.save()

    pp.pprint(stats)
    LOGGER.info('Wrote log file "{}"'.format(log_fname))


def run():
    ifname = "promrep/scripts/data/nicolet/NicoletExportv6.csv"

    LOGGER.info('Importing data from "{}"'.format(ifname))
    read_input_file(ifname)
