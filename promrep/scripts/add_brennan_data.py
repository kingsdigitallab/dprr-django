#!/usr/bin/python
# -*- coding: utf-8 -*-

# add_brennan_data.py

import csv

# U flag: universal new-line mode


def run():

    ifile = open('promrep/scripts/data/BrennanExportv5.csv', 'rU')
    reader = csv.reader(ifile, delimiter=',')

    i = 0
    for row in reader:
        print i

        date, page, note_ref, assertion_type, praenomen, nomen, re_number, filiation, cognomen, is_patrician, is_patrician_certainty, consular_ancestor, consular_ancestor_certainty, calculated_father, suggested_father, suggested_father_certainty, calculated_grandfather, suggested_grandfather, suggested_grandfather_certainty, brother, brother_certainty, more_remote, more_remote_certainty, novus, novus_certainty = row

        i = i+1

        print nomen

