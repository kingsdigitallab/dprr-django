# -*- coding: utf-8 -*-

## import csv
import unicodecsv as csv
import itertools
import logging
from os import path
import primary_source_aux as psource_aux

from promrep.models import (Person, StatusAssertion, Praenomen, Sex,
                            SecondarySource, StatusAssertionNote,
                            PostAssertion, Tribe, TribeAssertion)

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

    stats = {'person': {'new': 0, 'old': 0, 'found': 0}}

    with open(ifname, 'rU') as csvfile:

        csvDict = csv.DictReader(csvfile,
                                 fieldnames=ICSV_COLUMNS,
                                 delimiter=";")

        # skips header row
        csvDict.next()

        for row_dict in csvDict:

            person_id = int(row_dict['person'])

            if not person_id:
                person_dict = {
                    "praenomen": row_dict["praenomen"],
                    "nomen": row_dict["nomen"],
                    "re": row_dict["RE"],
                    "filiation": row_dict["filiation"],
                    "cognomen": row_dict["cognomen"],
                    "other_names": row_dict["other_names"]
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

            person = Person.objects.get(id=person_id)


            # always add the tribe info
            if row_dict['tribe']:
                for tribe in row_dict['tribe'].split(" or "):
                    tribe_str = tribe.strip()

                    if tribe_str:
                        # all tribes should already be in the db
                        try:
                            tribe_obj = Tribe.objects.filter(name__iexact=tribe_str).first()
                            tribe_uncertain = row_dict["tribe_uncertain"]

                            tribe_assertion, created = TribeAssertion.objects.get_or_create(person=person,
                                                                                            tribe=tribe_obj,
                                                                                            uncertain=tribe_uncertain,
                                                                                            secondary_source=sec_source)
                        except Exception as e:
                            LOGGER.error(e)
                            LOGGER.error(tribe_str)


            # original_text = row_dict["original_text"]

            # uncertain_flag = False
            # uncertain = row_dict["uncertain"].strip()
            # if uncertain:
            #     uncertain_flag = True

        # statys_assertion = StatusAssertion.objects.get_or_create()
        # always collect origin info

            #     # rel_notes = unicode(row_dict['notes'].strip(), 'iso-8859-1')

            #     rel_num = None
            #     marriage_no = row_dict["marriage_no"].strip()
            #     if marriage_no:
            #         rel_num = int(marriage_no)

            #     # create RelationshipAssertion
            #     # TODO: test if created
            #     rel, created = RelationshipAssertion.objects.get_or_create(
            #         person_id=p1_id, related_person_id=p2_id, relationship=rel_type,
            #         uncertain=uncertain_flag, secondary_source=sec_source,
            #         relationship_number=rel_num)

            #     if created:
            #         LOGGER.info(
            #             "Created new relationship with id={}".format(rel.id))
            #     else:
            #         LOGGER.info(
            #             "Relationship already existed with id={}".format(rel.id))

            #     rel.references.add(ra_reference)

            #     if created:
            #         # only creates the PrimarySourceReferences if the
            #         # RelAssertionRef was created
            #         for psource in primary_references_str.split(","):
            #             primary_reference = PrimarySourceReference(
            #                 content_object=ra_reference,
            #                 text=psource.strip())
            #             primary_reference.save()

            #     # Upgrades and saves the row
            #     row_dict.update({"p1_id": p1_id,
            #                      "relationshipassertion_id": rel.id,
            #                      "p2_id": p2_id})

            #     writer.writerow(row_dict)

            # except Exception as e:
            #     LOGGER.error(
            #         "Unable to import line from csv file... Please debug data. ".format(e.message))

    pp.pprint(stats)
    LOGGER.info("Wrote log file \"{}\"".format(log_fname))


def run():
    ifname = "promrep/scripts/data/nicolet/NicoletExportv4.csv"

    LOGGER.info("Importing data from \"{}\"".format(ifname))
    read_input_file(ifname)
