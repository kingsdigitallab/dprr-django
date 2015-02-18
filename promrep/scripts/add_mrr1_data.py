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

OFFICE_NAMES_DIC = {
    'aediles': 'aedilis',
    'aediles of the plebs': 'aedilis plebis',
    'aediles, curule': 'aedilis curulis',
    'aedilicii': 'aedilicius',
    'augures': 'augur',
    'augurs': 'augur',
    'censors': 'censor',
    'consul suffectus': 'consul suffectus',
    'consules designati': 'consul designatus',
    'consules suffecti': 'consul suffectus',
    'consuls': 'consul',
    'decemviri sacris faciundis': 'decemvir sacris faciundis',
    'flamen dialis': 'flamen dialis',
    'flamen divi iulii': 'flamen divi iulii',
    'flamen martialis': 'flamen martialis',
    'flamen quirinalis': 'flamen quirinalis',
    'flamens': 'flamen',
    'flamines': 'flamen',
    'flaminica martialis': 'flaminica martialis',
    'interreges': 'interrex',
    'iudices quaestionum': 'iudex quaestionis',
    'legates or prefects': 'legatus or praefectus',
    'legates, ambassadors': 'legatus',
    'legates, envoys': 'legatus',
    'legates, lieutenants': 'legatus',
    'luperci': 'lupercus',
    'master of horse': 'magister equitum',
    'masters of horse designate': 'magister equitum designatus',
    'pontifices': 'pontifex',
    'pontifices minores': 'pontifex minor',
    'praefectus urbi': 'praefectus urbis',
    'praetor suffectus': 'praetor suffectus',
    'praetores suffecti': 'praetor suffectus',
    'praetorii': 'praetorius',
    'praetors': 'praetor',
    'prefect of cavalry': 'praefectus equitum',
    'prefects': 'praefectus',
    'prefects of the city': 'praefectus urbis',
    'prefects of the fleet': 'praefectus classis',
    'prefects to assign land to veterans': 'praefectus agris dandis assignandis',
    'quaesitores': 'quaesitor',
    'quaestorii': 'quaestorius',
    'quaestors': 'quaestor',
    'quindecimviri sacris faciundis': 'quindecemvir sacris faciundis',
    'quindecimviri sacris fadundis': 'quindecemvir sacris faciundis',
    'quindeciniviri sacris faciundis': 'quindecemvir sacris faciundis',
    'quindecirnviri sacris faciundis': 'quindecemvir sacris faciundis',
    'quinqueviri agris dandis assignandis': 'quinquevir agris dandis assignandis',
    'rex sacrorum': 'rex sacrorum',
    'sacerdotes': 'sacerdos',
    'septemviri epulones': 'septemvir epulonum',
    'tribunes of the plebs': 'tribunus plebis',
    'tribunes of the soldiers': 'tribunus militum',
    'triumvir capitalis': 'triumvir capitalis',
    'triumviri capitales?': 'triumvir capitalis',
    'triumviri rei publicae constituendae': 'triumvir rei publicae constituendae',
    'vestal virgins': 'vestalis',
    'vestales': 'vestalis'
}

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
    # this is the file exported by OpenOffice

    ifile = 'promrep/scripts/data/mrr1_all_LF_Officesv14.docx.html.xml'
    print 'Will process input file', ifile
    processXML(ifile)


def processXML(ifile):
    page = file(ifile)
    soup = BeautifulSoup(page, features='xml')

    years = soup.findAll('year')

    # process year

    # for year in years[0:1]:
    for year in years:
        year_str = year['name'].split()[0]
        logger.debug("Parsing year %s" % (year_str))

        print
        print
        print ">>>>> Year", year_str, years.index(year), '(',len(year.findAll('footnote')), 'footnotes)'
        print


        # TODO: create a year note...

        # the footnotes can be added to a list
        # ... right at the "start" of the year

        # TODO:
        # ... we need to make sure all the refs agree with the footnotes
        # per ref we should:
        #  a) convert reference superscripts to lowercase/parentesis
        #  b) double-check if we have any other superscript

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

            #  every time a note is found, it is associated with
            #  all the assertion_persons in the list
            person_ref_queue = []

            assertion_type = AssertionType.objects.get(name='Office')

            source = SecondarySource.objects.get(abbrev_name='Broughton MRR I')

            assertion_date, created = AssertionDate.objects.get_or_create(
                        year = -int(year_str),
                    )

            assertion_dates_list = []
            assertion_dates_list.append(assertion_date)

            # tests if assertion already exists
            assertion_list = Assertion.objects.filter(office=office_obj,
                                                      assertion_type=assertion_type,
                                                      secondary_source=source,
                                                      dates__in = assertion_dates_list,
                                                      certainty = assertion_certainty)

            # if it doesn't exist, creates a new assertion
            if len(assertion_list) == 0:
                assertion = Assertion.objects.create(office=office_obj, assertion_type=assertion_type, secondary_source=source, certainty=assertion_certainty)

                for date in assertion_dates_list:
                    assertion.dates.add(date)
            elif len(assertion_list) == 1:
                assertion = assertion_list[0]
            else:
                # TODO: throw an Exception
                print "ERROR HERE! Multiple assertions with same basic info..."

            # add any existing notes to the assertion
            for onote in office_tag.find_all('office-note'):
                # print onote.get_text()
                a_note, created = AssertionNote.objects.get_or_create(text=onote.get_text())
                # print a_note
                assertion.notes.add(a_note)

            if office_tag.has_attr('footnote'):
                fnote_id = office_tag['footnote'].lstrip('#')

                if fnote_id in fnote_dict:
                    ofnote = fnote_dict[fnote_id]

                    afnote = AssertionNote(note_type=1, text = ofnote.get_text())
                    afnote.save()
                    assertion.notes.add(afnote)
                else:
                    print "ERROR adding office fnote" + fnote_id



            # Assertion: Office + Year + Person
            for p in office_tag.find_all('person'):
                print
                print "> Person:", p['name']
                name_el = p['name']

                # TODO: wrap in transaction
                try:
                    name_str = name_el

                    # parses person from name
                    person_info = aux.parse_person(name_str)

                    ######
                    # TODO: error handling???
                    ######
                    if person_info is None:
                        # will create a flagged person...
                        pass

                    # removes the date_certainty info from the dictionary
                    if 'date_certainty' in person_info:
                        ap_date_info = person_info.pop('date_certainty')
                    else:
                        ap_date_info = None

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
                        logger.info('Added new person %s with id %i' % (person.get_name(), person.id))

                    if person is not None:
                        # creates the AssertionPerson

                        yuncertain = False

                        if ap_date_info is not None:

                            if '?' in ap_date_info:
                                yuncertain = True
                            else:
                                print ap_date_info

                        date_start, created = AssertionPersonDate.objects.get_or_create(
                            year = -int(year_str),
                            year_uncertain = yuncertain
                        )

                        # TODO: stop creating repeated assertions
                        assertion_person, created = AssertionPerson.objects.get_or_create(
                            role=RoleType.objects.get(name='Holder'),
                            assertion=assertion,
                            person=person,
                            original_text = name_str,
                        )

                        # only adds this the first time the assertion is created
                        if created:
                            if p.has_attr('office-xref'):
                                assertion_person.office_xref=p['office-xref']
                                assertion_person.save()

                        assertion_person.dates.add(date_start)

                        # add any footnotes the person might have
                        if p.has_attr('footnote'):
                            fnote_id = p['footnote'].lstrip('#')

                            if fnote_id in fnote_dict:
                                pnote = fnote_dict[fnote_id]
                                ap_fnote = AssertionPersonNote(note_type=1, text = pnote.get_text())
                                ap_fnote.save()
                                assertion_person.notes.add(ap_fnote)
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
                                ref_text = ref_text + " " + r.get_text()

                                if r.has_attr('footnote'):
                                    footnotes.append(r['footnote'].lstrip('#'))

                            # creates the note
                            note, created = AssertionPersonNote.objects.get_or_create(
                                text=ref_text
                            )

                            notes_queue.append(note)

                            for fnote_id in footnotes:

                                if fnote_id in fnote_dict:
                                    apfnote_obj = fnote_dict[fnote_id]

                                    apfnote = AssertionPersonNote(note_type=1, text = apfnote_obj.get_text())
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
                                        extra_info = endnote_name
                                        )
                                    endnote.save()
                                    assertion.notes.add(endnote)
                                else:
                                    logger.error("Endnote error: %s" %(endnote_name))

                        except Exception as e:
                            logger.error('Error saving endnote: %s (%s)' % (e.message, type(e)))

                except Exception as e:
                    logger.error('%s' %(e.message))
