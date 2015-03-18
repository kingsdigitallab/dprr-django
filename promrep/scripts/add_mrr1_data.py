#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Adds the MRR1 data to the database

Usage:
  * Activate the virtual environment;
  * Run: python manage.py runscript promrep.add_mrr1_data

"""

from bs4 import BeautifulSoup

from promrep.models import ContentType, Assertion, AssertionPerson, \
  AssertionType, AssertionNote, AssertionDate, Office, Person, \
  RoleType, SecondarySource, AssertionPersonNote, AssertionPersonDate

import parsing_aux as aux
import logging

# TODO: configure in settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# add a file handler
fh = logging.FileHandler( 'mrr1_data_import.log')
fh.setLevel(logging.DEBUG)
# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(frmt)
# add the Handler to the logger
logger.addHandler(fh)

from promrep.scripts.offices_ref import OFFICE_NAMES_DIC

def get_office_obj(office_name):
    """given a string, returns an office object"""

    # convert to lowercase
    office_name = office_name.lower()

    # tries to get the normalized office name from the
    try:
        oname = OFFICE_NAMES_DIC[office_name]
    except:
        logger.warn("Unable to normalize office name: '%s'" %(office_name,))
        oname = office_name

    try:
        office = Office.objects.get(name=oname)
    except Office.DoesNotExist:

        # Adding new office
        #    in MRR all the offices are "civic" except for Vestal Virgin
        parent = Office.objects.get(name='Civic Offices')
        office = Office(name=oname, parent = parent)
        office.save()

        logger.info('Added Office: %s (id=%i)' % (office.name, office.id))

    return office



def run():
    processXML()


def processXML():

    volume = 'mrr1'

    sdict = {
        'mrr1': ['Broughton MRR I', 'promrep/scripts/data/mrr1_all_LF_Officesv18.docx.html.xml'],
        'mrr2': ['Broughton MRR II', 'promrep/scripts/data/mrr2_converted_html_v7.xml']
    }

    source = SecondarySource.objects.get( abbrev_name = sdict[volume][0] )
    ifile = sdict[volume][1]

    print
    print 'Will read', source, 'from file', ifile
    print

    page = file(ifile)
    soup = BeautifulSoup(page, features='xml')

    years = soup.findAll('year')

    # process year

    for year in years[0:5]:
    # for year in years:
        year_str = year['name'].split()[0]
        logger.debug("Parsing year %s" % (year_str))

        print
        print
        print ">>>>> Year", year_str, years.index(year), '(',len(year.findAll('footnote')), 'footnotes)'
        print

        # the footnotes can be added to a list
        # ... right at the "start" of the year
        fnote_dict = {}
        for fnote in year.findAll('footnote'):
            fnote_dict[fnote['ref']] = fnote

        # print fnote_dict

        # an assertion is defined by year, office, persons
        #   it can have associated notes
        #   and footnotes
        for office_tag in year.findAll('office'):

            # removes the spaces from the office name
            office_name = office_tag['name'].strip()

            print ">>> Office:", office_name

            assertion_certainty = True
            if "?" in office_name:
                # removes questionmark, marks assertion as uncertain
                office_name = office_name.strip('? ')
                assertion_certainty = False

            # get office using office name
            office_obj = get_office_obj(office_name)

            #  every time a note is found, it is associated with all the assertion_persons in the list
            person_ref_queue = []

            assertion_type = AssertionType.objects.get(name='Office')

            assertion_date = AssertionDate.objects.create(year = -int(year_str),)

            # tests if assertion already exists
            assertion_list = Assertion.objects.filter(office=office_obj,
                                                      assertion_type=assertion_type,
                                                      date__year = assertion_date.year,
                                                      certainty = assertion_certainty)

            # if it doesn't exist, creates a new assertion
            if len(assertion_list) == 0:
                assertion = Assertion.objects.create(office=office_obj, assertion_type=assertion_type, certainty=assertion_certainty)
                assertion_date.assertion = assertion
                assertion_date.save()

            elif len(assertion_list) == 1:
                assertion = assertion_list[0]
            else:
                # TODO: throw an Exception
                print "ERROR HERE! Multiple assertions with same basic info..."

            # add any existing notes to the assertion
            for onote in office_tag.find_all('office-note'):
                if onote.has_attr('name'):
                    a_note, created = AssertionNote.objects.get_or_create(text=onote['name'], secondary_source=source)
                    assertion.notes.add(a_note)

            if office_tag.has_attr('footnote') or office_tag.has_attr('x_footnote'):
                if office_tag.has_attr('footnote'):
                    fnote_id = office_tag['footnote'].lstrip('#')
                else:
                    fnote_id = office_tag['x_footnote'].lstrip('#')

                if fnote_id in fnote_dict:
                    ofnote = fnote_dict[fnote_id]

                    afnote = AssertionNote(note_type=1, text = ofnote.get_text(), secondary_source=source)
                    afnote.save()
                    assertion.notes.add(afnote)
                else:
                    print "ERROR adding office fnote" + fnote_id

            # Assertion: Office + Year + Person
            for p in office_tag.find_all('person'):

                name_str = p['name'].replace(u"’", "'").replace(u"\u2013", "-").replace(u'\xb4', "'")

                print
                print "> Person:", name_str

                try:
                    # parses person from name
                    person_info = aux.parse_person(name_str)

                    if person_info is None:
                        # creates as person with the whole name str as the nomen
                        person, created = Person.objects.get_or_create(nomen = name_str, review_flag=True)
                    else:
                        # removes the date_certainty info from the dictionary
                        if 'date_certainty' in person_info:
                            ap_date_info = person_info.pop('date_certainty').strip()
                        else:
                            ap_date_info = ""

                        # creates the person object from the dictionary directly
                        person, created = Person.objects.get_or_create(
                                                                praenomen = person_info['praenomen'],
                                                                nomen = person_info['nomen'],
                                                                real_number = person_info['real_number'],
                                                                )

                        # update the person's information
                        # updates all other relevant fields....
                        if created:
                            person.patrician = person_info.get('patrician', False)
                            person.praenomen_certainty = person_info.get('praenomen_certainty', True)
                            person.filiation = person_info.get('filiation', "")

                            if 'tribe' in person_info:
                                person.tribe = person_info['tribe']

                            person.cognomen = person_info.get('cognomen', "")
                            person.other_names = person_info.get('other_names', "")
                            person.patrician_certainty = person_info.get('patrician_certainty', False)
                            person.save()

                    if person is None:
                        print "ERROR creating person-->", name_str

                    # creates the AssertionPerson
                    else:
                        if p.has_attr('office-xref'):
                            oxref=p['office-xref']
                        else:
                            oxref=""

                        # TODO: stop creating repeated assertions
                        assertion_person, created = AssertionPerson.objects.get_or_create(
                            role=RoleType.objects.get(name='Holder'),
                            assertion=assertion,
                            secondary_source=source,
                            person=person,
                            original_text = name_str,
                            office_xref = oxref
                        )

                        # AssertionPerson Dates
                        ap_date_info = ap_date_info.strip("[:")

                        if ap_date_info:
                            ap_date = AssertionPersonDate.objects.create(year = -int(year_str), year_uncertain = True, assertion_person = assertion_person)

                            # cases that need manual fixing
                            if ap_date_info != "?":
                                ap_date.extra_info = ap_date_info
                                ap_date.save()

                        # AP certainty
                        if p.has_attr('assertion-certainty'):
                            assertion_person.certainty = False

                        # saves the order in the assertion
                        assertion_person.position = assertion.persons.count()
                        assertion_person.save()

                        # add any footnotes the person might have
                        if p.has_attr('footnote') or p.has_attr('x_footnote'):
                            if p.has_attr('footnote'):
                                fnote_id = p['footnote'].lstrip('#')
                            else:
                                fnote_id = p['x_footnote'].lstrip('#')

                            if fnote_id in fnote_dict:
                                pnote = fnote_dict[fnote_id]
                                try:
                                    ap_fnote = AssertionPersonNote(note_type=1, text = pnote.get_text(), secondary_source=source)
                                    ap_fnote.save()
                                    assertion_person.notes.add(ap_fnote)
                                except:
                                    print "ERROR ADDING NOTES!!!"
                            else:
                                print "ERROR adding person footnote with id", fnote_id

                        # adds the assertion_person to the refs queue
                        person_ref_queue.append(assertion_person)

                        # if the next element is a reference
                        #   we're adding it to all the assertions in the assertion queue
                        if p.findNextSibling().name == "references":
                            references = p.findNextSibling()
                            footnotes = []
                            notes_queue = []

                            ref_text = ""

                            # glues the ref parts together; mines footnotes
                            for r in references.findAll('ref'):
                                ref_text = ref_text + " " + r.get_text().strip()

                                if r.has_attr('footnote'):
                                    footnotes.append(r['footnote'].lstrip('#'))
                                elif r.has_attr('x_footnote'):
                                    footnotes.append(r['x_footnote'].lstrip('#'))

                            # creates the note
                            note, created = AssertionPersonNote.objects.get_or_create(
                                text=ref_text.strip(),
                                secondary_source=source
                            )

                            notes_queue.append(note)

                            for fnote_id in footnotes:
                                if fnote_id in fnote_dict:
                                    apfnote_obj = fnote_dict[fnote_id]
                                    apfnote = AssertionPersonNote(note_type=1, text = apfnote_obj.get_text().strip())
                                    apfnote.save()

                                    notes_queue.append(apfnote)

                                else:
                                    print "ERROR adding person footnote with id", fnote_id

                            for ap in person_ref_queue:

                                for n in notes_queue:
                                    ap.notes.add(n)

                            # resets the ref queue
                            person_ref_queue = []

                        try:
                            # tests if person has a bookmark/noteref
                            if p.find('noteref'):
                                endnote_name = p.noteref.get_text().strip('#')
                                endnote_text = year.find('note', bookmarks=endnote_name).get_text()

                                if endnote_text:
                                    endnote = AssertionPersonNote(
                                        text = endnote_text,
                                        note_type = NoteType.objects.get(name="Endnote"),
                                        extra_info = endnote_name,
                                        secondary_source = source
                                        )
                                    endnote.save()
                                    assertion.notes.add(endnote)
                                else:
                                    logger.error("Endnote error: %s" %(endnote_name))

                        except Exception as e:
                            logger.error('Error saving endnote: %s (%s)' % (e.message, type(e)))

                except Exception as e:
                    logger.error('%s' %(e.message))
