# -*- coding: utf-8 -*-

from os import path

import unicodecsv as csv
from promrep.models import (Office, Person, PostAssertion, Sex,
                            PostAssertionNote, Praenomen, SecondarySource,
                            Tribe, TribeAssertion)

ICSV_COLUMNS = ["person_id",
                "secondary_source",
                "post_assertion_note",
                "praenomen",
                "nomen",
                "re",
                "filiation",
                "cognomen",
                "other_names",
                "office_abbrev",
                "office_uncertain",
                "date_source_text",
                "date_start",
                "date_start_uncertain",
                "date_end",
                "date_end_uncertain",
                "tribe",
                "tribe_secondary_source",
                "tribe_note",
                "person_note",
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
    for field in ['nomen', 'cognomen', 'other_names', 'filiation']:
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
        print("Created person with id={}".format(person.id))

    return person.id, created


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


def update_person_from_csv_dict_row(person, row_dict):
    updated = False

    # Updates person empty fields
    # updates praenomen
    praenomen_str = row_dict["praenomen"].replace(
        "(", "").replace(")", "").strip("")

    if person.praenomen.abbrev == "-.":
        if praenomen_str not in ["-", ""]:
            praenomen_dict = get_praenomen_dict(praenomen_str)
            person.praenomen = praenomen_dict['praenomen']
            person.praenomen_uncertain = praenomen_dict.get(
                'praenomen_uncertain', False)

            updated = True
            print("DEBUG: Updated praenomen for person {}").format(person.id)

    # check if the csv has extra info
    for field in ["nomen", "filiation", "cognomen", "other_names"]:
        fvalue = row_dict[field].strip()

        if getattr(person, field) == "":
            if fvalue != "":
                setattr(person, field, fvalue)
                updated = True
                print("DEBUG: Updated field {} for person {}").format(
                    field, person.id)

    # RE case
    #  only update if existing is empty
    if person.re_number == "":
        re_str = row_dict['re'].strip()
        if re_str != "":
            person.re_number = re_str
            updated = True

    if updated:
        person.save()

    return person, updated


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
    log_fname = file_basename + "-log.csv"

    # log file with the ids of the objects created in the database
    csv_log = csv.DictWriter(
        open(log_fname, 'wb'),
        ["post_assertion_id", "person_id_new"] + ICSV_COLUMNS,
        dialect='excel',
        delimiter=",",
        extrasaction='ignore')
    csv_log.writeheader()

    with open(ifname, 'rU') as csvfile:

        csvDict = csv.DictReader(csvfile, fieldnames=ICSV_COLUMNS)

        # skips header row
        csvDict.next()

        for row_dict in csvDict:

            # tries to find teh person
            person_id = int(row_dict['person_id'])

            try:
                if person_id:
                    Person.objects.get(id=person_id)
            except:
                print("ERROR: person id does not exist: {}".format(person_id))
                person_id = 0

            if not person_id:
                person_dict = {
                    "praenomen": row_dict["praenomen"],
                    "nomen": row_dict["nomen"],
                    "re": row_dict["re"],
                    "filiation": row_dict["filiation"],
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

            person, updated = update_person_from_csv_dict_row(person, row_dict)

            # Secondary Source
            ssource_str = row_dict["secondary_source"]
            sec_source = get_sec_source_from_abbrev_str(ssource_str)

            # office info
            office, created = Office.objects.get_or_create(
                name=row_dict.get("office_abbrev"))

            print("Created new office {}".format(office))

            office_uncertain = row_dict.get("office_uncertain", 0)

            date_start = row_dict.get("date_start", None)

            date_start_uncertain = False
            if row_dict["date_start_uncertain"].strip():
                date_start_uncertain = True

            date_end = row_dict.get("date_end", None)

            date_end_uncertain = False
            if row_dict["date_end_uncertain"].strip():
                date_end_uncertain = True

            date_source_text = row_dict.get("date_source_text", "")

            # dates should be BC
            if date_start:
                try:
                    date_start = int(date_start)
                    if date_start > 0:
                        date_start = -date_start
                except:
                    print("ERROR: Date '{}' is not an integer."
                          .format(date_start))
                    date_start = None

            if date_end:
                try:
                    date_end = int(date_end)
                    if date_end > 0:
                        date_end = -date_end
                except:
                    print("ERROR: Date '{}' is not an integer."
                          .format(date_end))
                    date_end = None

            post_assertion = PostAssertion(
                person=person,
                office=office,
                uncertain=office_uncertain,
                date_start=date_start,
                date_start_uncertain=date_start_uncertain,
                date_end=date_end,
                date_end_uncertain=date_end_uncertain,
                date_source_text=date_source_text,
                secondary_source=sec_source
            )

            post_assertion.save()

            # only adds the note to the post assertion
            #    if there's text
            pa_note_text = row_dict.get("post_assertion_note", "")
            if pa_note_text:
                pa_note = PostAssertionNote.objects.create(
                    secondary_source=sec_source,
                    text=pa_note_text
                )

                post_assertion.notes.add(pa_note)
                post_assertion.save()

            # Tribe info
            if row_dict['tribe']:
                for tribe in row_dict['tribe'].split(" or "):
                    tribe_str = tribe.strip()

                    if tribe_str:
                        tribes = Tribe.objects.filter(name__iexact=tribe_str)
#
                        if tribes.count() == 0:
                            tribe_obj = Tribe.objects.create(
                                name=tribe_str, abbrev=tribe_str)
                        else:
                            tribe_obj = tribes.first()

                        tribe_ssource_str = row_dict["tribe_secondary_source"]
                        tribe_sec_source = get_sec_source_from_abbrev_str(
                            tribe_ssource_str)

                        # only created if doesn't exist already
                        # if tribe_obj not in person.tribes.all():
                        tr_assert, cr = TribeAssertion.objects.get_or_create(
                            person=person,
                            tribe=tribe_obj,
                        )

                        # only updates the secondary source if empty
                        if not tr_assert.secondary_source:
                            tr_assert.secondary_source = tribe_sec_source
                            tr_assert.save()

            row_dict.update({'person_id_new': person_id,
                             'post_assertion_id': post_assertion.id})
            csv_log.writerow(row_dict)

    print("Wrote log file \"{}\"".format(log_fname))


def run():
    ifname = "promrep/scripts/data/PostsFileV8.csv"

    print("Importing data from \"{}\"".format(ifname))
    read_input_file(ifname)
