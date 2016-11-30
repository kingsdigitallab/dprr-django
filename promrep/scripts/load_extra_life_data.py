# -*- coding: utf-8 -*-

# import csv
import csv
from os import path

from promrep.models import (
    DateInformation, DateType, Person, Praenomen, SecondarySource, Sex
)

ICSV_COLUMNS = [
    "person_id",
    "praenomen",
    "nomen",
    "re",
    "cognomen",
    "other_names",
    "date_1",
    "date_1_uncertain",
    "date_1_type",
    "date_1_ref",
    "date_1_notes",
    "date_2",
    "date_2_uncertain",
    "date_2_type",
    "date_2_ref",
    "date_2_notes",
    "date_3",
    "date_3_uncertain",
    "date_3_type",
    "date_3_ref",
    "date_3_notes",
    "date_4",
    "date_4_uncertain",
    "date_4_type",
    "date_4_ref",
    "date_4_notes",
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

    # cleans the remaining person name fields
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
        if field in row_dict:
            fvalue = row_dict[field].strip()

            if getattr(person, field) == "":
                if fvalue != "":
                    setattr(person, field, fvalue)
                    updated = True
                    print("DEBUG: Updated field {} for person {}").format(
                        field, person.id)

    # re case
    if person.re_number != "":
        re_str = row_dict['re'].strip()
        if re_str != "":
            person.re_number = re_str
            updated = True

    if updated:
        person.save()

    return person, updated


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
            print("DEBUG --> person_id {}".format(person_id)),

            try:
                if person_id:
                    # simply tries to check if the person exists...
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
                person, updated = update_person_from_csv_dict_row(person,
                                                                  row_dict)

                # can have up to 4 dates
                for i in range(1, 5):
                    date_str = row_dict['date_{}'.format(i)].strip()
                    date_ref = row_dict['date_{}_ref'.format(i)].strip()
                    uncertain_str = row_dict[
                        'date_{}_uncertain'.format(i)].strip()
                    date_type_str = row_dict['date_{}_type'.format(i)].strip()
                    date_note = row_dict['date_{}_notes'.format(i)].strip()

                    sec_source = False

                    if date_ref:
                        sec_source = get_sec_source_from_abbrev_str(date_ref)

                    if date_str:
                        # print i, row_dict

                        unc_flag = False
                        if uncertain_str:
                            unc_flag = True

                        date_type, created = DateType.objects.get_or_create(
                            name=date_type_str)

                        # date can be in intervals;
                        # if we have a before or after,
                        #    we'll only create a single point
                        interval = "S"

                        if "before" in date_str:
                            # B: Before
                            interval = "B"
                            date_str = date_str.replace('before', '').strip()
                            date_str = - int(date_str)
                        elif "after" in date_str:
                            # A: After
                            interval = "A"
                            date_str = date_str.replace('after', '').strip()
                            date_str = - int(date_str)
                        elif "by" in date_str:
                            # B: Before
                            interval = "B"
                            date_str = date_str.replace('by', '').strip()
                            date_str = - int(date_str) - 1
                        elif "AD" in date_str:
                            date_str = date_str.replace('AD', '').strip()
                            date_str = int(date_str)
                        else:
                            date_str = - int(date_str)

                        try:
                            di = DateInformation.objects.create(
                                person_id=person.id,
                                value=date_str,
                                uncertain=unc_flag,
                                date_type=date_type,
                                notes=date_note,
                                date_interval=interval
                            )

                            if sec_source:
                                di.secondary_source = sec_source
                                di.save()

                        except:
                            print("ERROR: Cannot create DateInformation"
                                  " object {}".format(row_dict))

                        print("Added {} to Person {}".format(di.id, person.id))

                row_dict.update({
                    'person_id_new': person_id
                })
                csv_log.writerow(row_dict)

            except Exception as e:
                print("ERROR: {}".format(e))

    print("Wrote log file \"{}\"".format(log_fname))


def run():
    ifname = "promrep/scripts/data/LifeDataOtherSourcesV2.csv"

    print("Importing data from \"{}\"".format(ifname))
    read_input_file(ifname)
