# -*- coding: utf-8 -*-

## import csv
import unicodecsv as csv
import itertools
import logging
from os import path
import primary_source_aux as psource_aux

from promrep.models import Person, RelationshipAssertion, Praenomen, \
    SecondarySource, PrimarySource, Sex, RelationshipType, RelationshipAssertionReference, \
    PrimarySourceReference

# Setup logging
LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
LOGGER.setLevel(logging.INFO)

ch = logging.StreamHandler()
log_formatter = logging.Formatter(u"%(levelname)s: [%(asctime)s] %(message)s")

ch.setFormatter(log_formatter)
LOGGER.addHandler(ch)

ICSV_COLUMNS = ["person_1_id",
                "person_1_sex",
                "person_1_praenomen",
                "person_1_nomen",
                "person_1_re",
                "person_1_cognomen",
                "person_1_other_names",
                "relationship",
                "uncertain",
                "marriage_no",
                "person_2_id",
                "person_2_sex",
                "person_2_praenomen",
                "person_2_nomen",
                "person_2_re",
                "person_2_cognomen",
                "person_2_other_names",
                "primary_source_refs",
                "ignore-me",
                ]


def clean_field(field, a_string):
    """cleans uncertain chars from a string, outputs a dictionary
    with the cleaned string and uncertainty flag
    """

    # chars to be removed from  most name fields
    unc_chars = ["?", ]
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
    """creates a new person object from a dictionary,
    and returns the new person id
    """

    person_dict = {}

    if row_dict['sex'].strip() == "F":
        sex = Sex.objects.get(name="Female")
    else:
        sex = Sex.objects.get(name="Male")

    person_dict['sex'] = sex

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

    print person_dict
    person, created = Person.objects.get_or_create(**person_dict)

    if created:
        LOGGER.info("Created person with id={}".format(person.id))
        person_dict["review_notes"] = "created from Zmeskal csv file"

    return person.id, created


def read_notes_file_to_dict(ifname):
    """ Reads a notes file to a dict
        returns a dictionary where the key is the reference name and the value is the note
    """

    notes_dict = {}

    # csvfile = codecs.open(ifname, 'r', encoding='latin1')
    csvfile = open(ifname, 'r')

    # with open(ifname, 'rU') as csvfile:

    csv_reader = csv.reader(csvfile, delimiter=";")

    for row in csv_reader:
        row_text = row[2].strip()
        notes_dict[row[1].strip()] = row_text

    csvfile.close()

    return notes_dict


def read_input_file(ifname, notes_csv_fname):

    file_basename = path.basename(ifname)
    file_basename = path.splitext(file_basename)[0]

    log_fname = file_basename + "_import-log.csv"

    # read the notes csv file
    notes_dict = read_notes_file_to_dict(notes_csv_fname)

    sec_source, created = SecondarySource.objects.get_or_create(
        name="Zmeskal family data", biblio="Zmeskal family data biblio entry",
        abbrev_name="Zmeskal")

    # log file with the ids of the objects created in the database
    writer = csv.DictWriter(open(log_fname, 'wb'),
                            ["person_1_id", "person_2_id",
                                "relationshipassertion_id"],
                            dialect='excel',
                            delimiter=";",
                            extrasaction='ignore')
    writer.writeheader()

    with open(ifname, 'rU') as csvfile:

        csvDict = csv.DictReader(csvfile,
                                 fieldnames=ICSV_COLUMNS,
                                 delimiter=";")

        # skips first row
        csvDict.next()

        for row_dict in csvDict:

            try:
                p1_id = int(row_dict['person_1_id'])
                p2_id = int(row_dict['person_2_id'])

                if not p1_id:
                    p1_dict = {
                        "sex": row_dict["person_1_sex"],
                        "praenomen": row_dict["person_1_praenomen"],
                        "nomen": row_dict["person_1_nomen"],
                        "re": row_dict["person_1_re"],
                        "cognomen": row_dict["person_1_cognomen"],
                        "other_names": row_dict["person_1_other_names"]
                    }

                    p1_id, created_p1 = create_person(p1_dict)
                    if created_p1:
                        LOGGER.info(
                            "Created new person1 with id {}".format(p1_id))
                    else:
                        LOGGER.info("Person1 id {}".format(p1_id))

                if not p2_id:
                    p2_dict = {
                        "sex": row_dict["person_2_sex"],
                        "praenomen": row_dict["person_2_praenomen"],
                        "nomen": row_dict["person_2_nomen"],
                        "re": row_dict["person_2_re"],
                        "cognomen": row_dict["person_2_cognomen"],
                        "other_names": row_dict["person_2_other_names"]
                    }

                    p2_id, created_p2 = create_person(p2_dict)
                    if created_p2:
                        LOGGER.info("Person2 created with id {}".format(p2_id))
                    else:
                        LOGGER.info(
                            "Person2 already existed with id {}".format(p2_id))

                # gets the relationship type from the csv file
                rel_type_name = row_dict["relationship"].strip().lower()

                rel_type, created = RelationshipType.objects.get_or_create(
                    name=rel_type_name)
                if created:
                    LOGGER.info(
                        "Created new relationship type {}".format(rel_type))

                uncertain_flag = False
                uncertain = row_dict["uncertain"].strip()
                if uncertain:
                    uncertain_flag = True

                # rel_notes = unicode(row_dict['notes'].strip(), 'iso-8859-1')

                rel_num = None
                marriage_no = row_dict["marriage_no"].strip()
                if marriage_no:
                    rel_num = int(marriage_no)

                # create RelationshipAssertion
                # TODO: test if created
                rel, created = RelationshipAssertion.objects.get_or_create(
                    person_id=p1_id, related_person_id=p2_id, relationship=rel_type,
                    uncertain=uncertain_flag, secondary_source=sec_source,
                    relationship_number=rel_num)

                if created:
                    LOGGER.info(
                        "Created new relationship with id={}".format(rel.id))
                else:
                    LOGGER.info(
                        "Relationship already existed with id={}".format(rel.id))

                # primary_source_refs cell parsing:
                #   Each line corresponds to a single RelationshipAssertionReference
                #   each cell may contain multiple comma-separated PrimarySourceReferences
                #   each cell can have a corresponding text Note (see notes file)
                #   The original reference is stored in the "extra_info" field

                # The relationship assertion reference is only created
                #   if it doesn't exist already.
                primary_references_str = row_dict[
                    'primary_source_refs'].strip()

                if primary_references_str in notes_dict:
                    ra_ref_text = notes_dict[primary_references_str]
                else:
                    ra_ref_text = ""

                # if text and primary sources are the same, then there's
                # no need to create a new secondary source
                ra_reference, created = RelationshipAssertionReference.objects.get_or_create(secondary_source=sec_source,
                                                                                             extra_info=primary_references_str,
                                                                                             text=ra_ref_text
                                                                                             )

                rel.references.add(ra_reference)

                if created:
                    # only creates the PrimarySourceReferences if the
                    # RelAssertionRef was created
                    for psource in primary_references_str.split(","):
                        primary_reference = PrimarySourceReference(
                            content_object=ra_reference,
                            text=psource.strip())
                        primary_reference.save()

                # Upgrades and saves the row
                row_dict.update({"p1_id": p1_id,
                                 "relationshipassertion_id": rel.id,
                                 "p2_id": p2_id})

                writer.writerow(row_dict)

            except Exception as e:
                LOGGER.error(
                    "Unable to import line from csv file... Please debug data. ".format(e.message))

    LOGGER.info("Wrote log file \"{}\"".format(log_fname))


def run():
    ifname = "promrep/scripts/data/zmeskal/ZmeskalOutv6.csv"

    # re-exported from excel as semicolon separated csv in utf8
    notes_csv = "promrep/scripts/data/zmeskal/zmeskal_from_xlsx.csv"

    LOGGER.info("Importing data from \"{}\"".format(ifname))

    read_input_file(ifname, notes_csv)
