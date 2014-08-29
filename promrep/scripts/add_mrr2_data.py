#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from promrep.models import ContentType, Assertion, AssertionPerson, AssertionType, \
    Date, Office, Person, RoleType, SecondarySource, Note

import data_import_aux
import logging

# create dictionary with name mapping
OFFICE_NAMES_DIC = {

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

            # some office names are sometimes added as plural
            try:
                office = Office.objects.get(name=office_name)

            except Office.DoesNotExist:
                # Adding new office
                # in MRR2 all offices are "civic" except for Vestal Virgin

                parent = Office.objects.get(name='Civic Offices')
                office = Office(name=office_name)
                office.parent = parent
                office.save()

                logger.info('Added Office: %s (id=%i)' %(office.name, office.id))


            for p in office_tag.find_all('person'):
                name_el = p.find('name')

                # get the next references block
                #### TODO.... sequential??
                references = p.findNext('references').get_text()

                ### TODO: wrap in transaction
                try:
                    name_str = name_el.get_text()
                    person = data_import_aux.parse_person_name(name_str)

                    try:
                        person.save()
                        logger.info('Saved person %s with id %i' %(person.name, person.id))
                    except Exception as e:
                        logger.error("Unable to save person %s" %(e.__cause__))
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
                        ### TODO: NoteType?
                        ### extra_info???
                        note = Note(text = references)
                        note.save()
                        try:
                            assertion.save()
                            if assertion:
                                assertion.notes.add(note)
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

                except Exception as e:
                    logger.error('%s (%s)' % (e.message, type(e)))
