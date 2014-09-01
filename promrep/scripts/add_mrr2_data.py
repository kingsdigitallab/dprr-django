#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from promrep.models import ContentType, Assertion, AssertionPerson, AssertionType, \
    Date, Office, Person, RoleType, SecondarySource, Note

import parsing_aux as aux
import logging

# create dictionary with name mapping
OFFICE_NAMES_DIC = {
    'Sacerdotes': 'Sacerdos',
    'Vestales': 'Vestalis',
    'Augures': 'Augur',
    'Civic Offices': 'Civic Office',
    'Aedile or Iudex Quaestionis': 'Aedilis or Iudex Quaestionis',
    'Aediles': 'Aedilis',
    'Aediles, Curule': 'Aedilis, Curulis',
    'Aediles of the Plebs': 'Aedilis, Plebis',
    'Aedilicii?': 'Aedilicius',
    'Augurs': 'Augur',
    'Censors': 'Censor',
    'Consules Designati': 'Consul Designatus', # should be beneath Consul?
    'Consules Suffecti': 'Consul Suffectus',  # should be beneath Consul?
    'Consuls': 'Consul',
    'Consul Suffectus': '',  # should be beneath Consul?
    'Decemviri Sacris Faciundis': 'Decemvir sacris faciundis',
    'Duumviri Perduellionis': 'Duumvir Perduellionis', # a special commission
    'Flamen Dialis': 'Flamen Dialis',
    'Flamen Divi Iulii': 'Flamen Divi Iulii',
    'Flamen Martialis': 'Flamen Martialis',
    'Flamen Quirinalis': 'Flamen Quirinalis',
    'Flamens': 'Flamen',
    'Flamines': 'Flamen',
    'Flaminica Martialis': 'Flaminica Martialis',
    'Interreges': 'Interrex',
    'Iudex Quaestionis': 'Iudex Quaestionis',
    'Iudices Quaestionum': 'Iudex Quaestionis',
    'Legates, Ambassadors': 'Legatus',
    'Legates, Ambassadors (or Lieutenants?)': 'Legatus',
    'Legates, Envoys': 'Legatus',
    'Legates, Envoys Group 1': 'Legatus',
    'Legates, Envoys Group 2': 'Legatus',
    'Legates, Envoys Group 3': 'Legatus',
    'Legates, Envoys Group 4': 'Legatus',
    'Legates, Lieutenants': 'Legatus',
    'Legates or Prefects': 'Legatus or Praefectus',
    'Luperci': 'Lupercus',
    'Master of Horse': 'Magister Equitum',
    'Masters of Horse Designate': 'Magister Equitum Designatus',
    'Pontifices': 'Pontifex',
    'Pontifices Minores': 'Pontifex Minor',
    'Praefectus Urbi': 'Praefectus Urbi',
    'Praetores Suffecti': 'Praetor Suffectus',
    'Praetorii': 'Praetorius',
    'Praetor or Iudex': 'Praetor or Iudex',
    'Praetor or Quaesitor': 'Praetor or Quaesitor',
    'Praetors': 'Praetor',
    'Praetor Suffectus': 'Praetor Suffectus',
    'Prefect of Cavalry': 'Praefectus Equitum',
    'Prefects': 'Praefectus',
    'Prefects of the City': 'Praefectus Urbis',
    'Prefects of the Fleet': 'Praefectus Classis',
    'Prefects to assign land to veterans': 'Praefectus agris dandis assignandis',
    'Promagistrates': '',
    'Quaesitores': 'Quaesitor',
    'Quaestorii': 'Quaestorius',
    'Quaestors': 'Quaestor',
    'Quindecimviri Sacris Faciundis': 'Quindecemvir Sacris Faciundis',
    'Quindecimviri Sacris Fadundis': 'Quindecemvir Sacris Faciundis',
    'Quindeciniviri Sacris Faciundis': 'Quindecemvir Sacris Faciundis',
    'Quindecirnviri Sacris Faciundis': 'Quindecemvir Sacris Faciundis',
    'Quinqueviri agris dandis assignandis': 'Quinquevir agris dandis assignandis',
    'Rex Sacrorum': 'Rex Sacrorum',
    'Salius': 'Salius', # not sure if a singular exists
    'Septemviri Epulones': 'Septemvir Epulonum',
    'Special Commission': '',
    'Special Commissions': '',
    'Special Commissions 1.': '',
    'Special Commissions 2.': '',
    'Special Commissions Curator viis sternendis': '',
    'Special Commissions Triumviri coloniis deducendis': '',
    'Tribunes of the Plebs': 'Tribunus Plebis',
    'Tribunes of the Soldiers': 'Tribunus Militum',
    'Triumvir Capitalis': 'Triumvir Capitalis',
    'Triumviri Capitales?': 'Triumvir Capitalis',
    'Triumviri Coloniis Ducendis': 'Triumvir Coloniis Ducendis', # a special commission
    'Triumviri Rei Publicae Constituendae': 'Triumvir Rei Publicae Constituendae',
    'Vestal Virgins': 'Vestalis'
}


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
    # this is the file exported by OpenOffice

    ifile = 'promrep/scripts/data/output-tidy-norefs.xml'
    print 'Will process input file', ifile
    processXML(ifile)

def processXML(ifile):
    page = file(ifile)
    soup = BeautifulSoup(page, features='xml')

    years = soup.findAll('year')

    for year in years:
        year_str = year.find('name').get_text().split()[0]
        logger.debug("Parsing year %s" %(year_str))

        for office_tag in year.findAll('office'):
            office_name = office_tag.find('name').get_text()

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

                logger.info('Added Office: %s (id=%i)' %(office.name, office.id))


            # empty list to hold the office's assertions
            #  every time a note is found, it is associated with
            #  all the people in this list
            #  the list is then cleared...
            assertion_ref_queue = []

            for p in office_tag.find_all('person'):
                name_el = p.find('name')


                ### TODO: wrap in transaction
                try:
                    name_str = name_el.get_text()
                    person = aux.parse_person(name_str)

                    try:
                        person.save()
                        logger.info('Saved person %s with id %i' %(person.get_name(), person.id))
                    except Exception as e:
                        logger.error("Unable to save person %s %s" %(name_str, e))

                        person = Person.objects.get(nomen = person.nomen, cognomen = person.cognomen, real_number = person.real_number)

                    if person != None:
                        # create both the assertion and the assertionperson objects
                        assertion_type = \
                            AssertionType.objects.get(name='Office')
                        source = \
                            SecondarySource.objects.get(abbrev_name='Broughton MRR II'
                                )
                        assertion = Assertion(office=office,
                                assertion_type=assertion_type,
                                secondary_source=source,
                                )

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


                        # if the next element is a note
                        #  we're adding it to all the assertions in the assertion queue
                        if p.findNextSibling().name == "references":
                            references = p.findNextSibling().get_text()

                            note = Note(text = references)
                            note.save()

                            for a in assertion_ref_queue:
                                a.notes.add(note)

                            # resets the ref queue
                            assertion_ref_queue = []


                except Exception as e:
                    logger.error('%s' %(e.message))
