#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

from promrep.models import ContentType, Post, PostAssertion, \
    PostType, Date, DateType, Office, Person, \
    Praenomen, RoleType, SecondarySource, Sex, Relationship, Note, NoteType

import parsing_aux
import logging

# TODO: configure in settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# add a file handler
fh = logging.FileHandler( 'data_import.log')
fh.setLevel(logging.DEBUG)
# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(frmt)
# add the Handler to the logger
logger.addHandler(fh)

def run():
    # U flag: universal new-line mode
    ifile = open('promrep/scripts/data/BrennanExportv6.csv', 'rU')
    reader = csv.reader(ifile, delimiter=',', skipinitialspace=True)

    next(reader, None)

    for original_row in reader:

        row = [a.strip() for a in original_row]

        (
            date_str,
            page,
            note_ref,
            assertion_type,
            praenomen_str,
            nomen,
            re_number,
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

        original_text = ' '.join(filter(None, [praenomen_str, nomen, cognomen]))

        if re_number:
            original_text = "%s (%s)" %(original_text, re_number)

        cognomen = ''
        other_names = ''

        if cognomen != '':
            cognomen_list = cognomen.split()

            cognomen = cognomen_list[0]

            if len(cognomen) > 1:
                other_names = ' '.join(cognomen_list[1:])

                # test for Tribe


        praenomen = None
        if praenomen_str != '':
            if praenomen_str.find('?') != -1:
                praenomen_str = praenomen_str.replace('?', '')

            try:
                praenomen = Praenomen.objects.get(abbrev=praenomen_str)

            except:
                try:
                    praenomen = Praenomen.objects.get(abbrev=praenomen_str + '.')

                except:
                    logger.error('Praenomen %s not found.' %(praenomen_str, ))

        print original_text

        parsed_person = Person(
            sex=Sex.objects.get(name='Male'),
            praenomen=praenomen,
            re_number=re_number,
            nomen=nomen.translate(None, "?()[]"),
            filiation=filiation,
            cognomen=cognomen,
            other_names=other_names,
            )

        if patrician == 'Patrician':
            parsed_person.patrician = True

        try:
            person = Person.objects.get(
                        praenomen = parsed_person.praenomen,
                        nomen = parsed_person.nomen,
                        re_number = parsed_person.re_number)

            person.update_empty_fields(parsed_person)
            logger.info('Updated existing person %s with id %i' %(person.get_name(), person.id))

        except Person.DoesNotExist:
            parsed_person.save()
            person = parsed_person
            logger.info('Added new person %s with id %i' %(person.get_name(), person.id))

        # TODO: test result
        add_office_assertion(person, date_str, original_text)

        # parsing the father
        if suggested_father != '':
            add_relationship_assertion(person, suggested_father, "Father")

        if suggested_grandfather != '':
            add_relationship_assertion(person, suggested_grandfather, "Grandfather")




def add_relationship_assertion(person, ancestor_str, rel_name):
    """ one of Father, Grandfather or More remote"""

    relationships_dic = {
        "Father": ["Son", "Father"],
        "Grandfather": ["Grandson", "Grandfather"],
        "More remote": ["Descendant", "Ancestor"]
    }

    print '[ancestor_str] ' + ancestor_str

    rel_assertion = Post(
        assertion_type=PostType.objects.get(name='Relationship'),
        relationship=Relationship.objects.get(name=rel_name),
        secondary_source=SecondarySource.objects.get(abbrev_name='Brennan Praetors'))
    rel_assertion.save()

    certainty = True

    # only one descendant - the current person
    desc_ap = PostAssertion(
        assertion = rel_assertion,
        person=person,
        role=RoleType.objects.get(name = relationships_dic[rel_name][0]),
        certainty = certainty)
    desc_ap.save()

    # can have multiple ancestors...
    if " or " in ancestor_str:
        ancestor_list = ancestor_str.split(" or ")
        certainty = False
        desc_ap.certainty = False
        desc_ap.save()
    else:
        ancestor_list = [ ancestor_str.strip() ]


    for ancestor_name in ancestor_list:
        ancestor_obj = parsing_aux.parse_brennan_person(ancestor_name)

        try:
            ancestor = Person.objects.get(
                praenomen = ancestor_obj.praenomen,
                nomen = ancestor_obj.nomen,
                re_number = ancestor_obj.re_number)

            logger.info('Found existing object (ancestor) %s with id %i' %(ancestor.get_name(), ancestor.id))
        except :
            ancestor_obj.save()
            ancestor = ancestor_obj

            logger.info('Saved ancestor object %s with id %i' %(ancestor.get_name(), ancestor.id))

        ancestor_ap = PostAssertion(
            assertion = rel_assertion,
            person=ancestor,
            role=RoleType.objects.get(name = relationships_dic[rel_name][1]),
            certainty = certainty,
            original_text=ancestor_str
            )

        ancestor_ap.save()







def add_office_assertion(person, date, original_text):

    source = SecondarySource.objects.get(abbrev_name='Brennan Praetors')
    office = Office.objects.get(name='praetor')
    assertion_type = PostType.objects.get(name='Office')
    praetor_role = RoleType.objects.get(name='Holder')

    ## TODO: wrap in a transaction
    try:
        assertion = Post(office=office,
                assertion_type=assertion_type,
                secondary_source=source)
        assertion.save()

        logger.info('Added new assertion id=%s' %(assertion.id))

    except:
        logger.error('Unable to save assertion.')

    try:
        ap = PostAssertion(
                role = praetor_role,
                assertion = assertion,
                person = person,
                original_text = original_text)
        ap.save()
        logger.info('Added new PostAssertion: %s' %(ap.id))

    except:
        logger.error('Unable to add new PostAssertion object.')

        # date_list = parse_brennan_date(date)
        # if date_list:
        #     for date in date_list:

        #         # need to test if date is not None
        #         if date:
        #             date.content_object = assertion
        #             try:
        #                 date.save()

        #             except e:
        #                 print e
        #                 print '[ERROR] Could not save date...' + date_str
        # else:
        #     print '[ERROR][DATE_PARSING]: ' + date_str







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

    if '<' in text:
        text = text.replace('<', '')

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
