#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from promrep.models import ContentType, Assertion, AssertionPerson, AssertionType, \
    Certainty, Date, DateType, Office, Person, Praenomen, RoleType, SecondarySource, Sex

import data_import_aux
import logging




# create dictionary with name mapping
OFFICE_NAMES_DIC = {



}



def run():
    # this is the file exported by OpenOffice

    logger = logging.getLogger(__name__)

    ifile = 'promrep/scripts/data/output-tidy-norefs.xml'
    print 'Will process input file', ifile
    processXML(ifile)

def processXML(ifile):
    page = file(ifile)
    soup = BeautifulSoup(page, features='xml')

    years = soup.findAll('year')

    error = 0
    exist = 0

    for year in years:
        year_str = year.find('name').get_text().split()[0]
        print "[DEBUG]Parsing year %s" %(year_str)

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

                print '[DEBUG][NEW_OFFICE] ', office, office.id


            for p in office_tag.find_all('person'):
                text = p.find('name')

                # get the next references block
                references = p.findNext('references').get_text()

                try:
                    text = text.get_text()

                    print "[DEBUG][FIND PERSON] ", text
                    person = data_import_aux.parse_person_name(text)

                    if person == None:
                        print "[ERROR]: Could not parse person: ", text
                    else:
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
                                    print '[DEBUG][NEW_PERSON] saved person with id', person.id
                                except:
                                    print '[ERROR] Unable to save person in the database.'
                            else:
                                print '[DEBUG][PERSON_EXISTS] person already in database with id=', person_exists
                                exist = exist + 1
                                person = Person.objects.get(pk=person_exists)


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

                                # adding the start date
                                #  end date depends on office??
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

                                except e:
                                    print e
                                    print '[ERROR] Could not save date...' + year_str

                                assertion_person = AssertionPerson(
                                    role=RoleType.objects.get(name='Holder'),
                                    assertion=assertion,
                                    person=person,
                                    original_text=references,
                                    )

                                try:
                                    assertion_person.save()

                                except:
                                    print "[ERROR][ASSERTION_PERSON] Could not save assertion person..."

                            except e:
                                print e
                                print "[ERROR][ASSERTION] Could not save assertion..."

                except Exception:

                    pass
