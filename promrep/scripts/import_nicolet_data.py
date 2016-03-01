# -*- coding: utf-8 -*-

## import csv
import unicodecsv as csv
import itertools
import logging
from os import path
import primary_source_aux as psource_aux

from promrep.models import (Person, StatusAssertion, Praenomen, Sex,
                            SecondarySource, StatusAssertionNote,
                            PostAssertion)

import pprint
pp = pprint.PrettyPrinter(width=1)

# Setup logging
LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
LOGGER.setLevel(logging.INFO)

ch = logging.StreamHandler()
log_formatter = logging.Formatter(u"%(levelname)s: [%(asctime)s] %(message)s")

ch.setFormatter(log_formatter)
LOGGER.addHandler(ch)

ICSV_COLUMNS = ["person",
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
                "notes"]


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
            a_string = a_string.replace(ch, '')

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

    person_dict['sex'] = Sex.objects.get(name="Male")

    if 'sex' in row_dict and row_dict['sex'].strip() == "F":
            person_dict['sex'] = Sex.objects.get(name="Female")

    # praenomen special case
    # we initially clean the string, and then add the object to the dictionary
    praenomen_str = row_dict.get('praenomen')
    if praenomen_str:
        if "." not in praenomen_str:
            praenomen_str = praenomen_str + "."

    praenomen_dic = clean_field('praenomen', praenomen_str)

    try:
        praenomen = Praenomen.objects.get(abbrev=praenomen_dic['praenomen'])
    except Praenomen.DoesNotExist:
        praenomen = Praenomen.objects.get(abbrev='-.')

    praenomen_dic['praenomen'] = praenomen

    # add praenomen info to person object
    person_dict.update(praenomen_dic)

    # cleans the remining person name fields
    for field in ['nomen', 'cognomen', 'other_names']:
        field_string = row_dict.get(field)

        if field_string:
            d_obj = clean_field(field, field_string)
            # updates the person dictionary
            person_dict.update(d_obj)

    # remaining person fields, where names were not standard
    person_dict['re_number'] = row_dict.get('re')

    # logger.info(person_dict)
    person, created = Person.objects.get_or_create(**person_dict)

    if created:
        LOGGER.info("Created person with id={}".format(person.id))
        person_dict["review_notes"] = "created from Zmeskal csv file"

    return person.id, created


def read_input_file(ifname):

    file_basename = path.basename(ifname)
    file_basename = path.splitext(file_basename)[0]

    log_fname = file_basename + "_import-log.csv"

    sec_source, created = SecondarySource.objects.get_or_create(
        name="Nicolet Equites Data", biblio="Nicolet Biblio Entry",
        abbrev_name="Nicolet")

    # log file with the ids of the objects created in the database
    writer = csv.DictWriter(open(log_fname, 'wb'),
                            ["person_1_id", "relationshipassertion_id"],
                            dialect='excel',
                            delimiter=";",
                            extrasaction='ignore')
    writer.writeheader()

    stats = { 'person': {'new': 0, 'old': 0, 'found': 0} }

    with open(ifname, 'rU') as csvfile:

        csvDict = csv.DictReader(csvfile,
                                 fieldnames=ICSV_COLUMNS,
                                 delimiter=";")

        # skips header row
        csvDict.next()

        # always collect tribe info
        for row_dict in csvDict:

            person_id = int(row_dict['person'])

            if not person_id:
                person_dict = {
                    "praenomen": row_dict["praenomen"],
                    "nomen": row_dict["nomen"],
                    "re": row_dict["RE"],
                    "filiation": row_dict["filiation"],
                    "cognomen": row_dict["cognomen"],
                    "other_names": row_dict["other_names"],
                    "person_original_text": row_dict["original_text"]
                }

                person_id, created = create_person(person_dict)
                if created:
                    stats['person']['new'] += 1
                    LOGGER.info("Added Person: id={}".format(person_id))
                else:
                    stats['person']['found'] += 1
                    LOGGER.info("Found Person: id={}".format(person_id))

            else:
                stats['person']['old'] += 1
                LOGGER.info("Lotus Person: id={}".format(person_id))


    pp.pprint(stats)
    LOGGER.info("Wrote log file \"{}\"".format(log_fname))


def run():
    ifname = "promrep/scripts/data/nicolet/NicoletExportv4.csv"

    LOGGER.info("Importing data from \"{}\"".format(ifname))
    read_input_file(ifname)
