# -*- coding: utf-8 -*-

import csv
from os import path

from promrep.models import (
    Person, Praenomen, SecondarySource, Sex, Tribe, TribeAssertion
)

ICSV_COLUMNS = [
    "person_id",
    "secondary_source",  # can be ignored
    "gender",
    "praenomen",
    "nomen",
    "filiation",
    "re",
    "cognomen",
    "other_names",
    "origin",
    "tribe",
    "tribe_secondary_source",
    "tribe_note",
    "person_note"
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


def get_praenomen_dict(praenomen_str):
    # praenomen special case
    # we initially clean the string, and then add the object to the dictionary

    if praenomen_str:
        if "." not in praenomen_str:
            praenomen_str = praenomen_str + "."

    praenomen_dict = clean_field('praenomen', praenomen_str)

    try:
        praenomen = Praenomen.objects.get(abbrev=praenomen_dict['praenomen'])
    except Praenomen.DoesNotExist:
        praenomen = Praenomen.objects.get(abbrev='-.')

    praenomen_dict['praenomen'] = praenomen

    return praenomen_dict


def create_person(row_dict):
    """Creates a new person object from a dictionary,
    and returns the new person id
    """

    person_dict = {}
    person_dict['sex'] = Sex.objects.get(name="Male")

    if 'sex' in row_dict and row_dict['sex'].strip() == "F":
        person_dict['sex'] = Sex.objects.get(name="Female")

    praenomen_dict = get_praenomen_dict(row_dict.get('praenomen'))

    # add praenomen info to person object
    person_dict.update(praenomen_dict)

    # cleans the remining person name fields
    for field in ['nomen', 'cognomen', 'other_names', 'filiation']:
        field_string = row_dict.get(field)

        if field_string:
            d_obj = clean_field(field, field_string)
            # updates the person dictionary
            person_dict.update(d_obj)

    # remaining person fields, where names were not standard
    person_dict['re_number'] = row_dict.get('re')

    print(person_dict)

    # logger.info(person_dict)
    person, created = Person.objects.get_or_create(**person_dict)

    if created:
        print("Created person with id={}".format(person.id))

    return person.id, created


def get_sec_source_from_abbrev_str(ssource_str):

    sec_source = None
    # tests if sec_source already exists
    slist = SecondarySource.objects.filter(abbrev_name=ssource_str)

    if len(slist) == 1:
        sec_source = slist.first()
    else:
        sec_source, cted = SecondarySource.objects.get_or_create(
            name=ssource_str + " Descriptive name",
            biblio=ssource_str + " Biblio",
            abbrev_name=ssource_str
        )

    return sec_source


def read_input_file(ifname):  # noqa
    file_basename = path.basename(ifname)
    file_basename = path.splitext(file_basename)[0]

    log_fname = file_basename + "_import-log.csv"

#    sec_source, created = SecondarySource.objects.get_or_create(
#        name="Nicolet Equites Data", biblio="Nicolet Biblio Entry",
#        abbrev_name="Nicolet")

    # log file with the ids of the objects created in the database
    csv_log = csv.DictWriter(open(log_fname, 'wb'),
                             ["person_id_new"] + ICSV_COLUMNS,
                             dialect='excel',
                             # delimiter=";",
                             extrasaction='ignore')
    csv_log.writeheader()

    with open(ifname, 'rU') as csvfile:
        csvDict = csv.DictReader(csvfile, fieldnames=ICSV_COLUMNS)

        # skips header row
        csvDict.next()

        for row_dict in csvDict:
            person_id = int(row_dict['person_id'])
            print("DEBUG: {}".format(person_id)),

            try:
                if person_id:
                    Person.objects.get(id=person_id)

                if not person_id:
                    person_dict = {
                        "praenomen": row_dict["praenomen"],
                        "nomen": row_dict["nomen"],
                        "re": row_dict["re"],
                        "filiation": row_dict.get("filiation", ""),
                        "cognomen": row_dict["cognomen"],
                        "other_names": row_dict["other_names"],
                        "review_flag": row_dict.get("review_flag", False)
                    }

                    person_id, created = create_person(person_dict)
                    if created:
                        print("Added Person: id={}".format(person_id))
                    else:
                        print("Found Person: id={}".format(person_id))

                else:
                    print("Found Person: id={}".format(person_id))

                person = Person.objects.get(id=person_id)

                # updates praenomen
                praenomen_str = row_dict["praenomen"]
                if person.praenomen.abbrev == "-.":
                    if praenomen_str != "-":
                        praenomen_dict = get_praenomen_dict(
                            row_dict.get('praenomen'))
                        person.praenomen = praenomen_dict['praenomen']
                        person.praenomen_uncertain = praenomen_dict.get(
                            'praenomen_uncertain', False)
                        print("Updated praenomen for person {}").format(
                            person.id)

                # check if the csv has extra info
                for field in ["nomen", "filiation", "cognomen",
                              "other_names", "origin"]:
                    fvalue = row_dict[field].strip()

                    if getattr(person, field) == "":
                        if fvalue != "":
                            setattr(person, field, fvalue)
                            print("Updated field {} for person {}").format(
                                field, person.id)

                # re case
                if person.re_number == "":
                    re_str = row_dict['re'].strip()
                    if re_str != "":
                        person.re_number = re_str

                person.save()

                # Tribe info
                if row_dict['tribe']:
                    tribe_notes = row_dict['tribe_note']
                    for tribe in row_dict['tribe'].split(","):
                        tribe_str = tribe.strip()

                        if tribe_str:
                            # TODO: tribes can be uncertain as well
                            tribe_uncertain = False
                            if "?" in tribe_str:
                                tribe_str = tribe_str.replace('?', '')
                                tribe_uncertain = True

                            tribes = Tribe.objects.filter(
                                name__iexact=tribe_str)
    #
                            if tribes.count() == 0:
                                tribe_obj = Tribe.objects.create(
                                    name=tribe_str, abbrev=tribe_str)
                            else:
                                tribe_obj = tribes.first()

                            tribe_ssource_str = row_dict[
                                "tribe_secondary_source"]
                            tribe_sec_source = get_sec_source_from_abbrev_str(
                                tribe_ssource_str)

                            # only created if doesn't exist already
                            # if tribe_obj not in person.tribes.all():
                            tr_assert, cr = \
                                TribeAssertion.objects.get_or_create(
                                    person=person,
                                    tribe=tribe_obj,
                                )

                            # only updates the secondary source if empty
                            if not tr_assert.secondary_source:
                                tr_assert.secondary_source = tribe_sec_source
                                tr_assert.save()

                            if not tr_assert.notes:
                                tr_assert.notes = tribe_notes
                                tr_assert.save()

                            if not tr_assert.uncertain:
                                tr_assert.uncertain = tribe_uncertain
                                tr_assert.save()

                row_dict.update({
                    'person_id_new': person_id
                })
                csv_log.writerow(row_dict)

            except Exception as e:
                print("ERROR: {}".format(e))

    print("Wrote log file \"{}\"".format(log_fname))


def run():
    ifname = "promrep/scripts/data/PersonsSampleFileV3.csv"

    print("Importing data from \"{}\"".format(ifname))
    read_input_file(ifname)
