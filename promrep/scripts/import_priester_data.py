
import unicodecsv as csv

from promrep.models import (Person, Praenomen, Sex, SecondarySource, )


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


def load_bio_data(ifname):
    """loads the person data from the csv file
    returns a dictionary with the name_original and
    the id of the person.
    """

    sec_source, created = SecondarySource.objects.get_or_create(
        name="Ruepke Data", biblio="Ruepke Data Biblio Entry",
        abbrev_name="Ruepke")

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
                    "ref_re",
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
                    "note",
                    "Input Date",
                    "Date_1",
                    "DateUncertain_1",
                    "DateType_1",
                    "Date_2",
                    "DateUncertain_2",
                    "DateType_2", ]

    # open CSV file
    with open(ifname, 'rU') as csvfile:

        # sweep csv file
        csv_line = csv.DictReader(csvfile,
                                  fieldnames=bio_csv_cols)

        # skips first row
        csv_line.next()

        for row_dict in csv_line:
            # print(row_dict)

            # TODO: can test life data to decide if we should ignore the person

            sex = Sex.objects.get(name="Male")

            if row_dict["sex"] != 'Mas.':
                sex = Sex.objects.get(name="Female")

            praenomen_str = row_dict.get('praenomen')

            if praenomen_str:
                if "." not in praenomen_str:
                    praenomen_str = praenomen_str + "."

            praenomen_dic = clean_field('praenomen', praenomen_str)

            try:
                praenomen = Praenomen.objects.get(
                    abbrev=praenomen_dic['praenomen'])
            except Praenomen.DoesNotExist:
                praenomen = Praenomen.objects.get(abbrev='-.')

            praenomen_dic['praenomen'] = praenomen

            # test if person exists
            p_arr = Person.objects.filter(
                nomen=row_dict["nomen"],
                sex=sex,
                praenomen=praenomen)

            if p_arr.count() == 0:
                print("Zero")
            elif p_arr.count() == 1:
                print("One")
            else:
                print("Plenty")

            # adding the notes to the person object
            # https://confluence.dighum.kcl.ac.uk/display/DPRR/Ruepke+Field+mapping

            # we should test and add all the person notes
            # even if the person already exists in the database

            # n_fields = ['ref',
            #             'ST',
            #             'LD',
            #             'P',
            #             'B',
            #             'RA',
            #             'L',
            #             'LA',
            #             'N',
            #             'other']

        return {}


def load_fastii_data(csv_fname, person_dict):
    """loads the fastii data from the csv file;
    needs a dictionary with the mapping between person names and id's
    """

    # we need to make the german notes be identified as such
    # PersonNote.objects.new()

    return True


def run():
    bio_csv_fname = "promrep/scripts/data/ruepke/ruepke_bio.csv"
    persons_dict = load_bio_data(bio_csv_fname)
    print(persons_dict)
