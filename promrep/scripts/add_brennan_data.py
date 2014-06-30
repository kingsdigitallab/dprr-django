#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

from promrep.models import ContentType, Assertion, AssertionPerson, \
    AssertionType, Certainty, Date, DateType, Office, Person, \
    Praenomen, RoleType, SecondarySource, Sex, Relationship

import data_import_aux


def run():

    # TODO: create stats class

    added = 0
    error = 0
    exist = 0

    # U flag: universal new-line mode

    ifile = open('promrep/scripts/data/BrennanExportv6.csv', 'rU')
    reader = csv.reader(ifile, delimiter=',', skipinitialspace=True)

    i = 1
    next(reader, None)  # skip the headers

    for original_row in reader:

        row = [a.strip() for a in original_row]

        (
            date_str,
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
            cognomen_first = cognomen_list[0]

            if len(cognomen) > 1:
                cognomen_other = ' '.join(cognomen_list[1:])

        if praenomen_str == '':
            praenomen = None
        else:

            # TODO: should attempt to parse the question mark

            if praenomen_str.find('?') != -1:
                praenomen = None
            else:
                try:
                    praenomen = \
                        Praenomen.objects.get(abbrev=praenomen_str)
                except:
                    try:
                        praenomen = \
                            Praenomen.objects.get(abbrev=praenomen_str
                                + '.')
                    except:
                        print '[ERROR]: Praenomen "' + praenomen_str \
                            + '" not found.'
                        praenomen = None

        person = Person(
            original_text=praenomen_str + ' ' + nomen + ' ' + filiation
                + ' ' + cognomen,
            sex=Sex.objects.get(name='Male'),
            praenomen=praenomen,
            real_number=real_number,
            nomen=nomen,
            filiation=filiation,
            cognomen_first=cognomen_first,
            cognomen_other=cognomen_other,
            consular_ancestor=False,
            is_patrician=False,
            )

        if patrician == 'Patrician':
            person.is_patrician = True

        print
        print '[DEBUG] Parsing line', i, '"' + nomen + ' (' \
            + real_number + ')"'

        person_exists = data_import_aux.person_exists(person)

        # test if person exists

        if person_exists == None:

            # TODO: how to handle this case?

            error = error + 1
        else:

            # no errors: the person either exists or will be created

            if person_exists == False:

                try:
                    person.save()
                    added = added + 1
                    print '[DEBUG] saved person with id', person.id
                except:

                    print '[ERROR] Unable to save person in the database.'
            else:

                exist = exist + 1
                person = Person.objects.get(pk=person_exists)

            add_office_assertion(person, 'Brennan Praetors', 'Praetors'
                                 , date_str)

            # parsing the father

            if suggested_father != '':

                print '[suggested_father]' + suggested_father

                father = \
                    data_import_aux.parse_person_name(suggested_father)

                if father != None:
                    father.save()

                    fs_assertion = \
                        Assertion(assertion_type=AssertionType.objects.get(name='Relationship'
                                  ),
                                  relationship=Relationship.objects.get(name='Father'
                                  ),
                                  secondary_source=SecondarySource.objects.get(abbrev_name='Brennan Praetors'
                                  ))
                    fs_assertion.save()

                    father = AssertionPerson(assertion=fs_assertion,
                            person=father,
                            role=RoleType.objects.get(name='Father'))
                    father.save()

                    son = AssertionPerson(assertion=fs_assertion,
                            person=person,
                            role=RoleType.objects.get(name='Son'))
                    son.save()

        i = i + 1

    print
    print 'Final Stats...'
    print '\tTotal entries in file:', i - 1
    print '\tNew persons (added to db):', added
    print '\tNot Added (already existed):', exist
    print '\tImport Errors:', error
    print


def add_office_assertion(
    person,
    source_abbrev,
    office_name,
    date_str,
    ):

    assertion_type = AssertionType.objects.get(name='Office')
    source = SecondarySource.objects.get(abbrev_name=source_abbrev)
    office = Office.objects.get(name=office_name)

    try:
        assertion = Assertion.objects.create(office=office,
                assertion_type=assertion_type, secondary_source=source)

        print '[DEBUG] Saved assertion with id', assertion.id

        date_list = parse_brennan_date(date_str)

        if date_list:

            for date in date_list:

                date.content_object = assertion

                try:
                    date.save()

                except e:
                    print e
                    print '[ERROR] Could not save date...' + date_str
        else:
            print '[ERROR][DATE_PARSING]: ' + date_str

        try:
            ap = \
                AssertionPerson.objects.create(role=RoleType.objects.get(name='Holder'
                    ), assertion=assertion, person=person)

            print '[DEBUG] Correctly created the AssertionPerson object with id', \
                ap.id
        except:

            print '[ERROR] Could not save AssertionPerson object...'
    except:

        print '[ERROR] Could not save assertion...'


def add_relationship_assertion(
    person1,
    person2,
    source_abbrev,
    relationship_name,
    ):

    assertion_type = AssertionType.objects.get(name='Relationship')
    source = SecondarySource.objects.get(abbrev_name=source_abbrev)
    relationship = Relationship.objects.get(name=relationship_name)

    try:
        assertion = Assertion.objects.create(relationship=relationship,
                assertion_type=assertion_type, secondary_source=source)

        print '[DEBUG] Saved assertion with id', assertion.id

        try:
            ap = \
                AssertionPerson.objects.create(role=RoleType.objects.get(name='Holder'
                    ), assertion=assertion, person=person)

            print '[DEBUG] Correctly created the AssertionPerson object with id', \
                ap.id
        except:

            print '[ERROR] Could not save AssertionPerson oject...'
    except:

        print '[ERROR] Could not save assertion...'


def parse_brennan_date(text):
    """Returns a tuple of Date with two objects
    If a date is not valid, it returns None on that tuple element
    If there any parsing issues, simply returns None """

    # we should always create two date objects
    date1 = Date(
        content_type=ContentType.objects.get(name='assertion'),
        interval=Date.DATE_MIN,
        year_uncertain=False,
        month_uncertain=False,
        day_uncertain=False,
        circa=False,
        )

    date2 = Date(
        content_type=ContentType.objects.get(name='assertion'),
        interval=Date.DATE_MAX,
        year_uncertain=False,
        month_uncertain=False,
        day_uncertain=False,
        circa=False,
        )

    # default office lenght
    duration = 1
    offset = 0

    if 'before' in text:
        text = text.replace('before', '')

        # will add the offset to the year
        #   before means that the year isn't included...
        offset = -1

        date1.interval = Date.DATE_MAX
        date2 = None

    if 'ca.' in text:
        text = text.replace('ca.', '')
        date1.circa = True
        date2 = None

    if '?' in text:
        # TODO: should also deal with ??/very uncertain
        text = text.replace('?', '')
        date1.year_uncertain = True

        if date2:
            date2.year_uncertain = True

    if 'by' in text:
        text = text.replace('by', '')

        date1.interval = Date.DATE_MAX
        date2 = None

    try:
        # all years are BC...
        year = int(text)
        if year > 0:
            year = -year

        date1.year = year + offset

        if date2:
            date2.year = date1.year + duration

        return [date1, date2]

    except ValueError, e:

        if 'c' in text:
            text = text.replace('c', '')

            # either ' or ' or '/'
            if '/' in text:
                century_parts = [-int(i)*100 for i in text.split('/')]

            elif ' or ' in text:
                century_parts = [-int(i)*100 for i in text.split(' or ')]
            else:
                # single value
                century_parts = [-int(text)*100, -int(text)*100]

            century_parts[1] = century_parts[1] + 99

            try:
                date1.year = century_parts[0]
                date2.year = century_parts[1]

                return (date1, date2)
            except:
                return None

        return None
