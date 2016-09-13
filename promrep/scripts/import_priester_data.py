
import unicodecsv as csv
from promrep.models import (
    DateInformation, DateType, NoteType, Office, Person, PersonNote,
    PostAssertion, Praenomen, SecondarySource, Sex
)


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


def add_post_assertion_to_person(person, row_dict, ssource):
    """Returns a PostAssertion object or None if unable to create it"""

    office, created = Office.objects.get_or_create(
        name=row_dict["office_abbrev"]
    )

    pa_dict = {
        "office": office,
        "person": person,
        "secondary_source": ssource
    }

    # date_source_text    date_start  date_start_uncertain    date_end
    # date_end_uncertain

    pa_dict["date_source_text"] = row_dict['date_source_text']

    pa_dict["date_start"] = - int(row_dict['date_start'])
    pa_dict["date_end"] = - int(row_dict['date_end'])

    pa_dict["date_start_uncertain"] = row_dict['date_start_uncertain']
    pa_dict["date_end_uncertain"] = row_dict['date_end_uncertain']

    pa_dict["uncertain"] = row_dict['uncertain']

    pa = PostAssertion.objects.create(**pa_dict)

    # TODO: return try:?
    return pa.id


def add_dates_to_person(person, row_dict, ssource):

    for n in ["1", "2"]:
        if row_dict["Date_" + n]:
            date_str = row_dict["Date_" + n]

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

            dtype, created = DateType.objects.get_or_create(
                name=row_dict["DateType_" + n])

            ddict = {
                "person": person,
                "value": date_str,
                "date_type": dtype,
                "uncertain": row_dict["DateUncertain_" + n],
                "secondary_source": ssource,
                "date_interval": interval
            }

            di, created = DateInformation.objects.get_or_create(**ddict)

            if created:
                print("Added new date {} to person {}".format(di, person.id))


def add_notes_fields_to_person(person, row_dict, ssource):
    """tests if the notes fields exist; if not adds these to the person object

    Does not return anything.
    """

    note_fields = [
        "ruepke_number",
        "Ref",
        "P",
        "ST",
        "LD",
        "B",
        "RA",
        "L",
        "LA",
        "N",
        "other",
    ]

    for note_field in note_fields:
        if row_dict[note_field]:
            ntext = row_dict[note_field]

            nt_str = note_field
            if "ruepke_" not in note_field:
                nt_str = "ruepke_" + note_field

            ntype, created = NoteType.objects.get_or_create(name=nt_str)

            note_dict = {
                'note_type': ntype,
                'text': ntext,
                'secondary_source': ssource
            }

            # test if note already exists
            notes = PersonNote.objects.filter(
                **note_dict).filter(person=person)

            # if note doesn't exist, we'll create it and add it to the person
            if not notes:
                note = PersonNote.objects.create(**note_dict)
                note.person_set.add(person)
                note.save()


def load_bio_data(ifname):
    """loads the person data from the csv file

    Returns a dictionary with all the person object fields.

    The Person objects will only be created/added when we process the
    fastii file.
    """

    persons_dict = {}

    bio_csv_cols = ["ruepke_number",
                    "sex",
                    "name_original",
                    "person_review_flag",
                    "praenomen",
                    "nomen",
                    "filiation",
                    "cognomen",
                    "other_names",
                    "patrician",
                    "re_number",
                    "Ref",
                    "P",
                    "ST",
                    "LD",
                    "B",
                    "RA",
                    "L",
                    "LA",
                    "N",
                    "other",
                    "Date_1",
                    "DateUncertain_1",
                    "DateType_1",
                    "Date_2",
                    "DateUncertain_2",
                    "DateType_2",
                    ]

    # open CSV file
    with open(ifname, 'rU') as csvfile:

        # sweep csv file
        csv_line = csv.DictReader(csvfile, fieldnames=bio_csv_cols)

        # skips first row
        csv_line.next()

        for row_dict in csv_line:

            # TODO: can test life data to decide if we should ignore the person

            person_dict = row_dict

            if row_dict["sex"] != 'Mas.':
                person_dict["sex"] = Sex.objects.get(name="Female")
            else:
                person_dict["sex"] = Sex.objects.get(name="Male")

            praenomen_orig = row_dict.get('praenomen')
            praenomen_str = praenomen_orig

            if praenomen_str:
                if "." not in praenomen_str:
                    praenomen_str = praenomen_str + "."

            praenomen_dic = clean_field('praenomen', praenomen_str)

            try:
                praenomen = Praenomen.objects.get(
                    abbrev=praenomen_dic['praenomen'])
            except Praenomen.DoesNotExist:
                praenomen = Praenomen.objects.get(abbrev='-.')

            person_dict['praenomen'] = praenomen

            if "?" in row_dict["patrician"]:
                person_dict['patrician_uncertain'] = True
            if "Patric." in row_dict["patrician"]:
                person_dict['patrician'] = True

            # will use either the ruepke number a tuple w/ names
            key_1 = row_dict["ruepke_number"].strip("-")

            key_2 = (
                praenomen_orig.strip().strip('.'),
                row_dict["nomen"],
            )

            if key_1:
                persons_dict.update({key_1: person_dict})
            else:
                persons_dict.update({key_2: person_dict})

    return persons_dict


def get_or_create_person(fas_row_dict, bio_dict, secondary_source):  # noqa
    """Returns a Person object or None if unable to create

    need to check if the notes have already been added to the person object
    """

    praenomen = fas_row_dict["praenomen"].strip('-')
    nomen = fas_row_dict["nomen"]
    ruepke_number = fas_row_dict["ruepke_number"].strip('-').strip()
    person_id = fas_row_dict["person_id"].strip('-').strip()

    # flag indicates if person was created
    created = False

    if ruepke_number:
        pdict = bio_dict[ruepke_number]
    else:
        pdict = bio_dict[(praenomen, nomen)]

    # when we cannot find info for the person
    if not pdict:
        return None, created

    if not pdict['nomen']:
        return None, created

    person_id = int(person_id)
    # most will already have a person_id
    if person_id:
        person = Person.objects.get(id=person_id)
    else:
        # if a person is created we add the person_id to the pdict
        # test if person exists; we start with at least the nomen
        p_arr = Person.objects.filter()

        params = [
            "sex",
            "praenomen",
            "nomen",
            "re_number",
        ]

        params_dict = {param: pdict[param]
                       for param in params if param in pdict}

        # for param in params:
        #     if pdict[param]:
        #         p_arr = p_arr.filter(**{param: pdict[param]})

        p_arr = p_arr.filter(**params_dict)

        if p_arr.count() == 0:
            # did not find a person - will create a person and then a PA
            # Person.objects.create()

            person = Person.objects.create(**params_dict)
            created = True

        elif p_arr.count() == 1:
            # found exactly one result - will create a new PA
            person = p_arr.first()

        else:
            # cannot create the postassertion
            # TODO: print error log
            return None, created

    # also updates all RE numbers to follow the fastii file
    if person.re_number != fas_row_dict["re"]:
        person.re_number = fas_row_dict["re"]
        person.save()
        print("Updated RE for {}".format(person.id))

    # extra info from Ruepke
    if "patrician" in pdict:
        person.patrician = True
        person.save()

    if "patrician_uncertain" in pdict:
        person.patrician_uncertain = True
        person.save()

    # TODO: should Ruepke info always supersede?
    if not person.cognomen and "cognomen" in pdict:
        person.cognomen = pdict["cognomen"]
        person.save()

    if not person.other_names and "other_names" in pdict:
        person.other_names = pdict["other_names"]
        person.save()

    # add filiation in case it's missing
    if not person.filiation and "filiation" in pdict:
        person.filiation = pdict["filiation"]
        person.save()

    add_notes_fields_to_person(person, pdict, secondary_source)
    add_dates_to_person(person, pdict, secondary_source)

    return person, created


def load_fastii_data(csv_fname, persons_dict):
    """loads the fastii data from the csv file;
    needs a dictionary with the person names and person data
    this will be used to search/add new persons as needed

    """

    ssource, created = SecondarySource.objects.get_or_create(
        name="Ruepke Data",
        biblio="Ruepke Data Biblio Entry",
        abbrev_name="Ruepke")

    fas_csv_cols = [
        "person_id",
        "ruepke_number",
        "secondary_source",
        "post_assertion_note_1",
        "praenomen",
        "nomen",
        "re",
        "filiation",
        "cognomen",
        "other_names",
        "office_abbrev",
        "uncertain",
        "date_source_text",
        "date_start",
        "date_start_uncertain",
        "date_end",
        "date_end_uncertain",
        "tribe_1",
        "tribe_secondary_source_1",
        "tribe_notes_1",
        "person_notes_1",
        "province_1",
        "province_uncertain_1",
        "province_notes_1"
    ]

    # output csv file file
    ocsv_fname = csv_fname.split("/")[-1].rstrip(".csv") + "-log.csv"

    # output file columns
    ocsv_cols = ["postassertion_id", "created_person"] + fas_csv_cols

    # open CSV files for reading and writing
    with open(csv_fname, 'rU') as csvfile, open(ocsv_fname, 'w') as ocsvfile:

        # sweep csv file
        csv_line = csv.DictReader(csvfile,
                                  fieldnames=fas_csv_cols,
                                  dialect='excel',
                                  delimiter=";")
        # skips first row
        csv_line.next()

        # writer for "log" file
        csv_writer = csv.DictWriter(
            ocsvfile,
            fieldnames=ocsv_cols,
            extrasaction='ignore'
        )
        csv_writer.writeheader()

        for row_dict in csv_line:
            pa_id = None
            created = False

            # if row_dict["name_lookup"]:
            #     person_name = row_dict["name_lookup"]

            person = None

            # gets a person object or None
            try:
                person, created = get_or_create_person(row_dict,
                                                       persons_dict,
                                                       ssource)

            except Exception as e:
                print e.__doc__
                print e.message

            # and creates the PostAssertion
            if person:
                pa_id = add_post_assertion_to_person(
                    person,
                    row_dict,
                    ssource)

                # used to write to the output csv file
                row_dict["postassertion_id"] = pa_id
                row_dict["person_id"] = person.id

                if created:
                    row_dict["created_person"] = person.id
                    row_dict["person_id"] = ""

            else:
                print("Unable to create PostAssertion")

            csv_writer.writerow(row_dict)

    return True


def run():
    bio_csv_fname = "promrep/scripts/data/ruepke/dprr_ruepke_bio-1.csv"
    persons_dict = load_bio_data(bio_csv_fname)

    fas_csv_fname = "promrep/scripts/data/ruepke/RuepkePostsOutV1.csv"
    load_fastii_data(fas_csv_fname, persons_dict)
