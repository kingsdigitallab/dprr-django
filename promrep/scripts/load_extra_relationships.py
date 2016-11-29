# -*- coding: utf-8 -*-

import csv
from os import path

from promrep.models import (
    Person, Praenomen, PrimarySourceReference, RelationshipAssertion,
    RelationshipAssertionReference, RelationshipType, SecondarySource, Sex
)

ICSV_COLUMNS = [
    "person_1_id",
    "person_1_name",
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
    "person_2_name",
    "person_2_sex",
    "person_2_praenomen",
    "person_2_nomen",
    "person_2_re",
    "person_2_cognomen",
    "person_2_other_names",
    "secondary_source",
    "primary_source_refs",
    "notes"
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
            a_string = a_string.replace(ch, '')

    dict_obj = {
        field: a_string,
    }

    if uncertain:
        dict_obj.update({field + "_uncertain": uncertain})

    return dict_obj


def create_or_update_person(person_idx, row_dict):  # noqa
    """person_idx indicates if it's person_1 or person_2
    row_dict is an entry on the input csv file

    this function checks is a person already exists; if so, enriches its info
    otherwise, creates a new person

    Returns a new person object"""

    person = None
    prefix = "person_" + person_idx

    person_id_str = row_dict[prefix + "_id"]
    if person_id_str is not "":
        person_id = int(person_id_str)
    else:
        person_id = 0

    if row_dict[prefix + '_sex'].strip() == "F":
        sex = Sex.objects.get(name="Female")
    else:
        sex = Sex.objects.get(name="Male")

    # praenomen special case
    # we initially clean the string, and then add the object to the dictionary
    praenomen_str = row_dict[prefix + "_praenomen"]

    # default case
    praenomen = Praenomen.objects.get(abbrev='-.')

    if praenomen_str:
        if "." not in praenomen_str:
            praenomen_str = praenomen_str + "."

    praenomen_dic = clean_field('praenomen', praenomen_str)

    try:
        praenomen = Praenomen.objects.get(abbrev=praenomen_dic['praenomen'])
    except Praenomen.DoesNotExist:
        print "Unable to find praenomen..."

    p_dict = {
        "sex": sex,
        "praenomen": praenomen,
        "re_number": row_dict[prefix + "_re"]
    }

    if "praenomen_uncertain" in praenomen_dic:
        p_dict["praenomen_uncertain"] = praenomen_dic["praenomen_uncertain"]

    for f in ["nomen", "cognomen", "other_names"]:
        f_clean = clean_field(f, row_dict[prefix + "_" + f])
        p_dict.update(f_clean)

    # default value
    person = None

    if person_id != 0:
        try:
            person = Person.objects.get(id=person_id)
        except:
            print("ERROR: Person with ID={} not in db".format(person_id))
            # we'll simply create this person from scratch...
            person_id = 0

    else:
        # cases where person_id = 0
        # the person mught have been created before
        p_list = Person.objects.filter(**p_dict)

        if len(p_list) == 1:
            person_id = p_list.first().id
            print("DEBUG: found person with same info {}".format(p_dict))
        elif len(p_list) == 0:
            print("DEBUG: couldn't find any matches for {}".format(p_dict))
        else:
            print("DEBUG: found too many matches for {}".format(p_dict))

    if not person_id:
        # only creates if person does not exist
        p_dict["review_notes"] = "created from extra_relationships.csv file"
        person = Person.objects.create(**p_dict)

        print("Created person with id={}".format(person.id))

    else:
        person = Person.objects.get(id=person_id)

        # update empty fields on existing person
        for field in p_dict.keys():
            if not getattr(person, field):
                setattr(person, field, p_dict[field])
                print("Updated {} for person {}".format(field, person.id))
                person.save()

    return person


def get_sec_source_from_abbrev_str(ssource_str):

    sec_source = None
    ssource_str = ssource_str.strip()

    # workaround to make sure source names match the db
    if ssource_str == "Brennan":
        ssource_str = "Brennan Praetors"
    elif ssource_str == "Badian":
        ssource_str = "Badian Consuls"

    # tests if sec_source already exists
    slist = SecondarySource.objects.filter(
        abbrev_name__iexact=ssource_str.strip())

    if len(slist) == 1:
        sec_source = slist.first()
    else:
        sec_source, cted = SecondarySource.objects.get_or_create(
            name=ssource_str + " Descriptive name",
            biblio=ssource_str + " Biblio",
            abbrev_name=ssource_str
        )
        if cted:
            print("DEBUG>>CREATED SSOURCE: {} {}".format(
                sec_source,
                ssource_str))

    return sec_source


def read_input_file(ifname):  # noqa

    file_basename = path.basename(ifname)
    file_basename = path.splitext(file_basename)[0]

    log_fname = file_basename + "-log.csv"

    # log file with the ids of the objects created in the database
    writer = csv.DictWriter(open(log_fname, 'wb'),
                            ["p1_id", "p2_id",
                                "relationshipassertion_id"] + ICSV_COLUMNS,
                            dialect='excel',
                            extrasaction='ignore')
    writer.writeheader()

    with open(ifname, 'rU') as csvfile:

        csvDict = csv.DictReader(csvfile, fieldnames=ICSV_COLUMNS)

        # skips first row
        csvDict.next()

        for row_dict in csvDict:

            p1 = create_or_update_person("1", row_dict)
            p2 = create_or_update_person("2", row_dict)

            # gets the relationship type from the csv file
            rel_type_name = row_dict["relationship"].strip().lower()

            rel_type, created = RelationshipType.objects.get_or_create(
                name=rel_type_name)
            if created:
                print("Created new relationship type {}".format(rel_type))

            uncertain_flag = False
            uncertain = row_dict["uncertain"].strip()
            if uncertain:
                uncertain_flag = True

            # rel_notes = unicode(row_dict['notes'].strip(), 'iso-8859-1')

            rel_num = None
            marriage_no = row_dict["marriage_no"].strip()
            if marriage_no:
                rel_num = int(marriage_no)

            ssource_str = row_dict["secondary_source"].strip()
            sec_source = get_sec_source_from_abbrev_str(ssource_str)

            ra_dict = {
                "person_id": p1.id,
                "related_person_id": p2.id,
                "relationship": rel_type,
                "uncertain": uncertain_flag,
            }

            if len(RelationshipAssertion.objects.filter(**ra_dict)):
                print("Duplicate relationship found: {}".format(ra_dict))
            else:
                ra_dict["secondary_source"] = sec_source
                ra_dict["relationship_number"] = rel_num

                # create RelationshipAssertion
                rel, created = RelationshipAssertion.objects.get_or_create(
                    **ra_dict)

                if created:
                    print("Created new relationship with id={}".format(rel.id))

                    # The relationship assertion reference is only created
                    #   if it doesn't exist already.
                    primary_references_str = row_dict[
                        'primary_source_refs'].strip()

                    if primary_references_str:
                        ra_reference, created = \
                            RelationshipAssertionReference.\
                            objects.get_or_create(
                                secondary_source=sec_source,
                                extra_info=primary_references_str,
                            )
                        rel.references.add(ra_reference)

                        # create individual PrimarySourceReferences only if
                        # created the ra_ref
                        if created:
                            for psource in primary_references_str.split(","):
                                primary_reference = PrimarySourceReference(
                                    content_object=ra_reference,
                                    text=psource.strip())
                                primary_reference.save()
                else:
                    print("Relationship already existed with id={}".format(
                        rel.id))

            # Upgrades and saves the row
            row_dict.update({"p1_id": p1.id,
                             "relationshipassertion_id": rel.id,
                             "p2_id": p2.id})

            writer.writerow(row_dict)

    print("Wrote log file \"{}\"".format(log_fname))


def run():
    ifname = "promrep/scripts/data/NewRelationshipsOtherV3.csv"

    print("Importing data from \"{}\"".format(ifname))
    read_input_file(ifname)
