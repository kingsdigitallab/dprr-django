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
        # print i
        # drop first row (header)
        if i == 0:
            pass
        else:
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

            if praenomen_str == '':
                praenomen = None
            else:

                if praenomen_str.find('?') != -1:
                    praenomen = None
                else:
                    try:
                        praenomen = Praenomen.objects.get(abbrev=praenomen_str)
                    except:
                        try:
                            praenomen = Praenomen.objects.get(abbrev=praenomen_str + '.')
                        except:
                            print "ERROR: praenomen not found..."
                            praenomen = None

            if patrician == 'Patrician':
                is_patrician = True
            else:
                is_patrician = False

            person = Person(
                original_text=praenomen_str + ' ' + nomen + ' '
                    + filiation + ' ' + cognomen,
                sex=Sex.objects.get(name='Male'),
                praenomen=praenomen,
                real_number=real_number,
                nomen=nomen,
                filiation=filiation,
                cognomen_first=cognomen_first,
                cognomen_other=cognomen_other,
                is_patrician=is_patrician,
                is_noble=False,
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

            if res != False:
                add_brennan_praetor_assertion(person)

        i = i + 1

    print
    print 'Final Stats...'
    print '\tTotal entries in file:', i - 1
    print '\tNew persons (added to db):', added
    print '\tNot Added (already existed):', exist
    print '\tImport Errors:', error
    print


def add_brennan_praetor_assertion(person):

    source = SecondarySource.objects.get(abbrev_name='Brennan Praetors')
    assertion_type = AssertionType.objects.get(name='Office')
    office = Office.objects.get(name='Praetors')

    assertion = Assertion(office=office, assertion_type=assertion_type,
                          secondary_source=source)

    try:
        assertion.save()

        assertion_person = \
            AssertionPerson(role=RoleType.objects.get(name='Holder'),
                            assertion=assertion, person=person)

        try:
            assertion_person.save()
        except:
            print '[ERROR SAVING ASSERTION PERSON OBJECT]'
    except:

        print '[ERROR SAVING ASSERTION]'
