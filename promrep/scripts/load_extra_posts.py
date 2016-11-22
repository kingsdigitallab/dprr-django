# -*- coding: utf-8 -*-

import re
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
        print("Created person with id={}".format(person.id))

    return person.id, created


def read_input_file(ifname):  # noqa

    file_basename = path.basename(ifname)
    file_basename = path.splitext(file_basename)[0]

    # log file with the ids of the objects created in the database
    csv_log = csv.DictWriter(open("extra_posts.log", 'wb'),
                             ["person_id", "person", "post_assertion"],
                             dialect='excel',
                             delimiter=";",
                             extrasaction='ignore')
    csv_log.writeheader()

    with open(ifname, 'rU') as csvfile:

        csvDict = csv.DictReader(csvfile,
                                 fieldnames=ICSV_COLUMNS,
                                 delimiter=";")

        # skips header row
        csvDict.next()

        for row_dict in csvDict:

            person_id = int(row_dict['person_id'])

            if not person_id:
                person_dict = {
                    "praenomen": row_dict["praenomen"],
                    "nomen": row_dict["nomen"],
                    "re": row_dict["RE"],
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

            # create the secondary sources
            sec_source = None
            ssource_str = row_dict["secondary_source"]

            slist = SecondarySource.objects.filter(
                abbrev_name=ssource_str)

            if len(slist) == 1:
                sec_source = slist.first()
            else:
                sec_source, cted = SecondarySource.objects.get_or_create(
                    name=ssource_str + " Descriptive name",
                    biblio=ssource_str + " Biblio",
                    abbrev_name=ssource_str
                )

            # add the tribe info
            if row_dict['tribe']:
                for tribe in row_dict['tribe'].split(" or "):
                    tribe_str = tribe.strip()

                    if tribe_str:
                        tribes = Tribe.objects.filter(name__iexact=tribe_str)

                        if tribes.count() == 0:
                            tribe_obj = Tribe.objects.create(
                                name=tribe_str, abbrev=tribe_str)
                        else:
                            tribe_obj = tribes.first()

                        tribe_uncertain = row_dict["tribe_uncertain"]

                        # only created if doesn't exist already
                        if tribe_obj not in person.tribes.all():
                            tr_assert, cr = \
                                TribeAssertion.objects.get_or_create(
                                    person=person,
                                    tribe=tribe_obj,
                                    uncertain=tribe_uncertain,
                                    secondary_source=sec_source)

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
                    office_name = row_dict['office_name'].strip()
                    office_list = Office.objects.filter(
                        name__iexact=office_name)

                    if len(office_list):
                        office = Office.objects.get(name__iexact=office_name)
                    else:
                        office, created = Office.objects.get_or_create(
                            name=office_name)

                    pa_assertion, created = \
                        PostAssertion.objects.get_or_create(
                            person=person,
                            office=office,
                            secondary_source=sec_source,
                            date_source_text=date_source_text,
                            uncertain=row_dict['office_uncertain'],
                            original_text=row_dict['original_text'],
                            review_flag=row_dict['review_flag']
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
                    print row_dict["notes"]
                    pa_txt = re.sub(
                        r"(Nicolet\sRef\s[0-9]+\.).*", r"\1",
                        row_dict["notes"])
                    print pa_txt

                    # adds the note to the post assertion
                    pa_note = PostAssertionNote.objects.create(
                        secondary_source=sec_source,
                        text=pa_txt,)

                    pa_assertion.notes.add(pa_note)
                    pa_assertion.save()


def run():
    ifname = "promrep/scripts/data/PostsFileV1.csv"

    print("Importing data from \"{}\"".format(ifname))
    read_input_file(ifname)
