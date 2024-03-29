import csv
import itertools
import logging

from promrep.models import (Office, Person, PostAssertion, PostAssertionNote,
                            PostAssertionProvince, Praenomen, Province,
                            SecondarySource)

# Setup logging
LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
LOGGER.setLevel(logging.INFO)

ch = logging.StreamHandler()
log_formatter = logging.Formatter(u"%(levelname)s: [%(asctime)s] %(message)s")

ch.setFormatter(log_formatter)
LOGGER.addHandler(ch)


def clean_field(field, a_string):
    """cleans uncertain chars from a string, outputs a dictionary
    with the cleaned string and uncertainty flag
    """

    # chars to be removed from  most name fields
    unc_chars = [
        "?",
    ]
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


def create_post_assertion(row_dict, p_id):
    """creates a post assertion, returns its id"""

    post_assertion = {}
    office, created = Office.objects.get_or_create(
        name="monetalis", abbrev_name="monetal."
    )
    source, created = SecondarySource.objects.get_or_create(
        name="Monetalis source record name",
        biblio="Monetalis source record biblio",
        abbrev_name="monetalis abbrev name",
    )

    if row_dict["review_later"]:
        post_assertion["review_flag"] = True

    post_assertion["office_id"] = office.id
    post_assertion["role_id"] = 1
    post_assertion["secondary_source_id"] = source.id
    post_assertion["person_id"] = p_id

    post_assertion["date_source_text"] = row_dict["date_source_text"]

    date_start = row_dict.get("date_start")
    if int(date_start):
        post_assertion["date_start"] = -int(date_start)

    if row_dict["start_uncertain"] == "0":
        post_assertion["date_start_uncertain"] = False
    else:
        post_assertion["date_start_uncertain"] = True

    date_end = row_dict.get("date_end")
    if int(date_end):
        post_assertion["date_end"] = -int(date_end)

    if row_dict["end_uncertain"] == "0":
        post_assertion["date_end_uncertain"] = False
    else:
        post_assertion["date_end_uncertain"] = True

    post_assertion["date_secondary_source_id"] = source.id

    post_assertion["original_text"] = row_dict["original_name_text"]

    # create a new post assertion
    pa = PostAssertion.objects.create(**post_assertion)
    LOGGER.info("New PostAssertion saved with id={}".format(pa.id))

    # create/attach provinces to the post assertion
    if row_dict["location"] != "":
        province_name = row_dict["location"].strip()
        pa.province_original = row_dict["location"].strip()
        pa.save()

        if "?" in province_name:
            province_name = province_name.strip("?").strip()
            province_uncertain = True
        else:
            province_uncertain = False

        province, created = Province.objects.get_or_create(name=province_name)

        PostAssertionProvince.objects.create(
            province=province, post_assertion=pa, uncertain=province_uncertain
        )

    # create/attach the notes to the post assertion
    if row_dict["note_ref"]:
        for note_ref in row_dict["note_ref"].split(","):
            text = "ref. " + note_ref
            pa_note = PostAssertionNote.objects.create(
                text=text, secondary_source=source, note_type_id=1
            )

            pa.notes.add(pa_note)

    return pa.id


def create_person(row_dict):
    """creates a new person object from a dictionary,
    and returns the new person id
    """

    person_dict = {}
    person_dict["review_notes"] = "created by upload_RRC script"
    # Male
    person_dict["sex_id"] = 1

    # we are not setting any defaults when getting these keys
    # because we prefer to fail loudly if a key is missing...
    if row_dict["review_later"]:
        person_dict["review_flag"] = True

    # praenomen special case
    # we initiall clean the string, and then add the object to the dictionary
    praenomen_str = row_dict.get("praenomen")
    praenomen_dic = clean_field("praenomen", praenomen_str)

    try:
        praenomen = Praenomen.objects.get(abbrev=praenomen_dic["praenomen"])
    except Praenomen.DoesNotExist:
        praenomen = Praenomen.objects.get(abbrev="-.")

    praenomen_dic["praenomen"] = praenomen

    # add praenomen info to person object
    person_dict.update(praenomen_dic)

    # cleans the remining person name fields
    for field in ["nomen", "cognomen", "other_names", "filiation"]:
        field_string = row_dict.get(field)

        if field_string:
            d_obj = clean_field(field, field_string)
            # updates the person dictionary
            person_dict.update(d_obj)

    # remaining person fields, where names were not standard
    person_dict["re_number"] = row_dict.get("re")

    person = Person.objects.create(**person_dict)

    return person.id


def lower_underscore_first(iterator):
    """converts uppercase to lowercase and replaces spaces with underscores"""
    return itertools.chain([next(iterator).lower().strip().replace(" ", "_")], iterator)


def read_input_file(ifname):
    writer = csv.DictWriter(
        open("monetales_v7_log.csv", "wb"),
        ["original_name_text", "person_id", "postassertion_id"],
        dialect="excel",
        delimiter=";",
        extrasaction="ignore",
    )
    writer.writeheader()

    with open(ifname, "rU") as csvfile:

        csvDict = csv.DictReader(lower_underscore_first(csvfile), delimiter=";")

        for row_dict in csvDict:
            p_id = int(row_dict["person_id"])

            if row_dict["person_id"] == "0":
                p_id = create_person(row_dict)
                LOGGER.info("Created new person with id {}".format(p_id))
            else:
                LOGGER.info("Person already existed in the database;")

            # create a new PostAssertion
            pa_id = create_post_assertion(row_dict, p_id)

            # upgrades and saves the row
            row_dict.update({"person_id": p_id, "postassertion_id": pa_id})
            writer.writerow(row_dict)


def run():
    datafilename = "promrep/scripts/monetales/RRCExportv7.txt"
    read_input_file(datafilename)
