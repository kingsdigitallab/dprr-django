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
    'Dictator': 'dictator',
    'Sacerdotes': 'sacerdos',
    'Vestales': 'vestalis',
    'Augures': 'augur',
    'Aedile or Iudex Quaestionis': 'aedilis or iudex quaestionis',
    'Aediles': 'aedilis',
    'Aediles, Curule': 'aedilis curulis',
    'Aediles of the Plebs': 'aedilis plebis',
    'Aedilicii?': 'aedilicius',
    'Augurs': 'augur',
    'Censors': 'censor',
    'Consules Designati': 'consul designatus',
    'Consules Suffecti': 'consul suffectus',
    'Consuls': 'consul',
    'Consul Suffectus': 'consul suffectus',
    'Decemviri Sacris Faciundis': 'decemvir sacris faciundis',
    'Flamen Dialis': 'flamen dialis',
    'Flamen Divi Iulii': 'flamen divi Iulii',
    'Flamen Martialis': 'flamen Martialis',
    'Flamen Quirinalis': 'flamen Quirinalis',
    'Flamens': 'flamen',
    'Flamines': 'flamen',
    'Flaminica Martialis': 'flaminica Martialis',
    'Interreges': 'interrex',
    'Iudex Quaestionis': 'iudex quaestionis',
    'Iudices Quaestionum': 'iudex quaestionis',
    'Legates, Ambassadors': 'legatus',
    'Legates, Ambassadors (or Lieutenants?)': 'legatus',
    'Legates, Envoys': 'legatus',
    'Legates, Envoys Group 1': 'legatus',
    'Legates, Envoys Group 2': 'legatus',
    'Legates, Envoys Group 3': 'legatus',
    'Legates, Envoys Group 4': 'legatus',
    'Legates, Lieutenants': 'legatus',
    'Legates or Prefects': 'legatus or praefectus',
    'Luperci': 'lupercus',
    'Master of Horse': 'magister equitum',
    'Masters of Horse Designate': 'magister equitum designatus',
    'Pontifices': 'pontifex',
    'Pontifices Minores': 'pontifex minor',
    'Praefectus Urbi': 'praefectus urbis',
    'Praetores Suffecti': 'praetor suffectus',
    'Praetorii': 'praetorius',
    'Praetor or Iudex': 'praetor or iudex',
    'Praetor or Quaesitor': 'praetor or quaesitor',
    'Praetors': 'praetor',
    'Praetor Suffectus': 'praetor suffectus',
    'Prefect of Cavalry': 'praefectus equitum',
    'Prefects': 'praefectus',
    'Prefects of the City': 'praefectus urbis',
    'Prefects of the Fleet': 'praefectus classis',
    'Prefects to assign land to veterans':
    'praefectus agris dandis assignandis',
    'Promagistrates': 'Promagistrates', # check this - are there sub categories
    'Quaesitores': 'quaesitor',
    'Quaestorii': 'quaestorius',
    'Quaestors': 'quaestor',
    'Quindecimviri Sacris Faciundis': 'quindecemvir sacris faciundis',
    'Quindecimviri Sacris Fadundis': 'quindecemvir sacris faciundis',
    'Quindeciniviri Sacris Faciundis': 'quindecemvir sacris faciundis',
    'Quindecirnviri Sacris Faciundis': 'quindecemvir sacris faciundis',
    'Quinqueviri agris dandis assignandis':
    'quinquevir agris dandis assignandis',
    'Rex Sacrorum': 'rex sacrorum',
    'Salius': 'salius',
    'Septemviri Epulones': 'septemvir epulonum',
    'Special Commission': 'Special Commission from Caesar to collect a library', # in the year 45
    'Special Commissions Decemviri agris dandis assignandis': 'decemvir agris dandis assignandis', # in the year 91
    'Special Commissions Quinqueviri agris dandis assignandis': 'quinquevir agris dandis assignandis', # in the year 91
    'Special Commissions Duumviri Perduellionis': 'duumvir perduellionis', # in the year 63
    'Special Commissions' : 'triumvir agris dividendis', # in the year 41
    'Special Commissions 1.': 'duodecemvir agris dandis assignandis', # in the year 59
    'Special Commissions 1.': 'duumvir actis Caesaris confirmandis', # in the year 44
    'Special Commissions 2.': 'quinquevir agris dandis assignandis iudicandis',  # in the year 59
    'Special Commissions 2.': 'septemvir agris dividendis',  # in the year 44
    'Special Commissions Curator viis sternendis': 'curator viis sternendis', # in the year 93
    'Special Commissions Triumviri coloniis deducendis': 'triumvir coloniis deducendis', # in the year 80
    'Tribunes of the Plebs': 'tribunus plebis',
    'Tribunes of the Soldiers': 'tribunus militum',
    'Triumvir Capitalis': 'triumvir capitalis',
    'Triumviri Capitales?': 'triumvir capitalis',
    'Triumviri Rei Publicae Constituendae': 'triumvir rei publicae constituendae',
    'Vestal Virgins': 'vestalis'
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

    ifile = 'promrep/scripts/data/mrr1_all_MR_Officesv12.docx.html_.xml'
    print 'Will process input file', ifile
    processXML(ifile)


def processXML(ifile):
    page = file(ifile)
    soup = BeautifulSoup(page, features='xml')

    years = soup.findAll('year')

    # process year

    #for year in years[-2:]:
    for year in years:
        year_str = year['name'].split()[0]
        logger.debug("Parsing year %s" % (year_str))

        print
        print
        print ">>>>>FNOTES", year_str, years.index(year)
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

            office_name = office_tag['name']
            print ">>", office_name

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
                                                      dates__in = assertion_dates_list)

            # if it doesn't exist, creates a new assertion
            if len(assertion_list) == 0:
                assertion = Assertion.objects.create(office=office_obj, assertion_type=assertion_type, secondary_source=source, )
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


                        # TODO: special case for Successor?
                        # TODO: stop creating repeated assertions
                        assertion_person, created = AssertionPerson.objects.get_or_create(
                            role=RoleType.objects.get(name='Holder'),
                            assertion=assertion,
                            person=person,
                            original_text = name_str,
                        )

                        assertion_person.dates.add(date_start)

                        # add any footnotes the person might have
                        if p.has_attr('footnote'):
                            fnote_id = p['footnote'].lstrip('#')

                            if fnote_id in fnote_dict:
                                pnote = fnote_dict[fnote_id]
                                ap_fnote = AssertionPersonNote(note_type=1, text = ofnote.get_text())
                                ap_fnote.save()
                                assertion_person.notes.add(ap_fnote)
                            else:
                                print "ERROR adding person footnote with id", fnote_id

                        # adds the assertion_person to the refs queue
                        person_ref_queue.append(assertion_person)

                        # if the next element is an AssertionPerson
                        #  we're adding it to all the assertions in the assertion queue
                        if p.findNextSibling().name == "references":
                            references = p.findNextSibling()

                            # TODO: test footnotes
                            ref_text = ""
                            for r in references.findAll('ref'):
                                ref_text = ref_text + " " + r.get_text()

                            note, created = AssertionPersonNote.objects.get_or_create(
                                text=ref_text
                            )


                            for ap in person_ref_queue:
                                ap.notes.add(note)

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
