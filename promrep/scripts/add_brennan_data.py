#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

from promrep.models import Assertion, AssertionPerson, AssertionType, \
    Certainty, Date, DateType, Office, Person, Praenomen, RoleType, \
    SecondarySource, Sex

import data_import_aux


def run():

    added = 0
    error = 0
    exist = 0

    # U flag: universal new-line mode

    ifile = open('promrep/scripts/data/BrennanExportv6.csv', 'rU')
    reader = csv.reader(ifile, delimiter=',', skipinitialspace=True)

    i = 0

    for row in reader:
        print i
        if i == 0:
            pass
        else:

            # dealing with leading/trailing whitespaces

            (
                date,
                page,
                note_ref,
                assertion_type,
                praenomen_str,
                nomen,
                real_number,
                filiation,
                cognomen,
                patrician,
                patrician_certainty,
                consular_ancestor,
                consular_ancestor_certainty,
                calculated_father,
                suggested_father,
                suggested_father_certainty,
                calculated_grandfather,
                suggested_grandfather,
                suggested_grandfather_certainty,
                brother,
                brother_certainty,
                more_remote,
                more_remote_certainty,
                novus,
                novus_certainty,
                province,
                blank,
                ) = row

            cognomen_first = ''
            cognomen_other = ''

            if cognomen != '':
                cognomen_list = cognomen.split()

                if len(cognomen) > 1:
                    cognomen_first = cognomen_list[0]
                    cognomen_other = ' '.join(cognomen_list[1:])
                else:
                    cognomen_first = cognomen_list[0]

            # TODO: fix...
            if praenomen_str != '':
                print praenomen_str

                if praenomen_str.find("?") != -1:
                    praenomen = None
                elif praenomen_str.find('.') == -1:
                    try:
                        praenomen = Praenomen.objects.get(abbrev=praenomen_str + '.')
                    except:
                        praenomen = None

            else:
                praenomen = None

            if patrician == "Patrician":
                is_patrician = True
            else:
                is_patricia = False

            person = Person(
                original_text = praenomen_str + ' ' + nomen + ' ' + filiation + ' ' + cognomen,
                sex=Sex.objects.get(name='Male'),
                praenomen=praenomen,
                real_number=real_number,
                nomen=nomen,
                filiation=filiation,
                cognomen_first=cognomen_first,
                cognomen_other=cognomen_other,
                is_patrician = is_patrician,
                is_noble = False
                )

                # is_patrician=is_patrician,
                # is_noble=False,

            # test if person exists

            res = data_import_aux.add_new_person_to_db(person)

            if res == True:
                added = added + 1
            elif res == None:
                exist = exist + 1
            else:
                error = error + 1

        i = i + 1

    print
    print "Total: ", i-1, "Added: ", added, "Existing: ", exist, "Errors: ", error


def add_brennan_assertion():

    source = SecondarySource.objects.get(abbrev_name='Brennan Praetors')
    assertion_type = AssertionType.objects.get(name='Office')
