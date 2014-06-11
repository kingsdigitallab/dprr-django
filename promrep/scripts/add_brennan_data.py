#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

from promrep.models import Assertion, AssertionPerson, AssertionType, \
    Certainty, Date, DateType, Office, Person, Praenomen, RoleType, \
    SecondarySource, Sex

import promrep.scripts.data_import_aux

def run():

    # U flag: universal new-line mode

    ifile = open('promrep/scripts/data/BrennanExportv6.csv', 'rU')
    reader = csv.reader(ifile, delimiter=',')

    for row in reader:

        (
            date,
            page,
            note_ref,
            assertion_type,
            praenomen,
            nomen,
            real_number,
            filiation,
            cognomen,
            is_patrician,
            is_patrician_certainty,
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

        # test if person exists




        data_import_aux.

        identic_persons = Person.objects.filter(nomen=nomen.strip(),
                real_number=real_number.strip())

        if identic_persons.count() > 1:




        print note_ref.strip(), blank.strip()


        # print "testing ", nomen.strip(), real_number.strip(), identic_persons.count()

        # print nomen
