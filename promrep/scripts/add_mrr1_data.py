#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Adds the MRR1 data


Usage:

Activate the virtual environment;

python manage.py runscript add_mrr1_data

"""

from bs4 import BeautifulSoup

from promrep.models import ContentType, Assertion, AssertionPerson, \
  AssertionType, AssertionNote, PersonNote, Date, Office, Person, \
  RoleType, SecondarySource, PersonNote, AssertionNote

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


def run():
    # this is the file exported by OpenOffice

    ifile = 'promrep/scripts/data/mrr1_all_MR_Officesv12.docx.html_.xml'
    print 'Will process input file', ifile
    processXML(ifile)


def processXML(ifile):
    page = file(ifile)
    soup = BeautifulSoup(page, features='xml')

    years = soup.findAll('year')

    for year in years:

        year_str = year['name'].split()[0]
        logger.debug("Parsing year %s" % (year_str))

        for office_tag in year.findAll('office'):
            office_name = office_tag['name']
            print office_name

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
                # in MRR2 all offices are "civic" except for Vestal Virgin

                parent = Office.objects.get(name='Civic Offices')
                office = Office(name=oname)
                office.parent = parent
                office.save()

                logger.info('Added Office: %s (id=%i)' % (office.name, office.id))

            # empty list to hold the office's assertions
            #  every time a note is found, it is associated with
            #  all the people in this list
            #  the list is then cleared...
            assertion_ref_queue = []

            # Assertion: Office + Year + Person
            for p in office_tag.find_all('person'):

                name_el = p['name']

                ### TODO: wrap in transaction
                try:
                    name_str = name_el

                    # parses person from name
                    parsed_person = aux.parse_person(name_str)

                    # TODO: error handling???
                    if parsed_person is None:
                        print name_str

                    try:
                        person = Person.objects.get(
                            praenomen=parsed_person.praenomen,
                            nomen=parsed_person.nomen,
                            real_number=parsed_person.real_number)

                        person.update_empty_fields(parsed_person)

                        logger.info('Updated existing person %s with id %i' %
                                    (person.get_name(), person.id))

                    except Person.DoesNotExist:
                        parsed_person.save()
                        person = parsed_person

                        logger.info('Added new person %s with id %i' %
                                    (person.get_name(), person.id))

                    if person is not None:

                        # create both the assertion and assertionperson objects
                        assertion_type = AssertionType.objects.get(
                            name='Office')

                        source = SecondarySource.objects.get(
                            abbrev_name='Broughton MRR I')

                        assertion = Assertion(
                            office=office,
                            assertion_type=assertion_type,
                            secondary_source=source,)

                        try:
                            assertion.save()

                            ### adds the assertion to the refs queue
                            assertion_ref_queue.append(assertion)

                            date_start = Date(
                                content_type=ContentType.objects.get(name='assertion'),
                                interval=Date.DATE_MIN,
                                year = -int(year_str),
                                year_uncertain=False,
                                month_uncertain=False,
                                day_uncertain=False,
                                circa=False,
                            )
                            date_start.content_object = assertion

                            try:
                                date_start.save()
                            except Exception as e:
                                logger.error('Unable to save date...' + year_str)
                            assertion_person = AssertionPerson(
                                role=RoleType.objects.get(name='Holder'),
                                assertion=assertion,
                                person=person,
                                original_text = name_str,
                                )
                            try:
                                assertion_person.save()
                            except:
                                logger.error("[ERROR][ASSERTION_PERSON] Could not save assertion person...")

                        except Exception as e:
                            logger.error('Error saving assertion: %s (%s)' % (e.message, type(e)))


                        try:
                            # if the next element is a note
                            #  we're adding it to all the assertions in the assertion queue
                            if p.findNextSibling().name == "references":
                                references = p.findNextSibling().get_text()

                                note = Note(
                                    text=references,
                                    note_type=NoteType.objects.get(name="Reference"),
                                    )

                                note.save()

                                for a in assertion_ref_queue:
                                    a.notes.add(note)

                                # resets the ref queue
                                assertion_ref_queue = []

                        except Exception as e:
                            logger.error('Error saving reference notes: %s (%s)' % (e.message, type(e)))

                        try:
                            # tests if person has a bookmark/noteref
                            if p.find('noteref'):
                                endnote_name = p.noteref.get_text().strip('#')
                                endnote_text = year.find('note', bookmarks=endnote_name).get_text()


                                if endnote_text:
                                    endnote = Note(
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
