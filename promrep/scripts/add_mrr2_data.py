#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from promrep.models import ContentType, Post, PostAssertion, PostType, \
    Date, Office, Person, RoleType, SecondarySource, Note, NoteType

import parsing_aux as aux
import logging

from promrep.scripts.offices_ref import OFFICE_NAMES_DIC

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

                    # parses person from name
                    parsed_person = aux.parse_person(name_str)

                    try:
                        person = Person.objects.get(
                                praenomen = parsed_person.praenomen,
                                nomen= parsed_person.nomen,
                                re_number=parsed_person.re_number)

                        person.update_empty_fields(parsed_person)
                        logger.info('Updated existing person %s with id %i' %(person.get_name(), person.id))

                    except Person.DoesNotExist:
                        parsed_person.save()
                        person = parsed_person
                        logger.info('Added new person %s with id %i' %(person.get_name(), person.id))


                    if person != None:
                        # create both the assertion and the PostAssertion objects
                        assertion_type = \
                            PostType.objects.get(name='Office')
                        source = \
                            SecondarySource.objects.get(abbrev_name='Broughton MRR II'
                                )
                        assertion = Post(office=office,
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
                            post_assertion = PostAssertion(
                                role=RoleType.objects.get(name='Holder'),
                                assertion=assertion,
                                person=person,
                                original_text = name_str,
                                )
                            try:
                                post_assertion.save()
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
                                    text = references,
                                    note_type = NoteType.objects.get(name="Reference"),
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
