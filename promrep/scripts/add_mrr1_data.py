#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Adds the MRR1 data to the database

Usage:
  * Activate the virtual environment;
  * Run: python manage.py runscript promrep.add_mrr1_data

"""

from bs4 import BeautifulSoup

from promrep.models import Post, PostAssertion, PostNote, Office, Person, \
    RoleType, SecondarySource, PostAssertionNote, Praenomen

import parsing_aux as aux
from promrep.scripts.offices_ref import OFFICE_NAMES_DIC

def parse_post_assertion_date(ap_date_info, post_year):

    # default case
    obj = {'date_source_text': ap_date_info,
           'review_flag': False,
           'date_start': -int(post_year),
           'date_end': -int(post_year)}

    if ap_date_info == "?":
        obj['date_start_uncertain'] = True

    elif "-" in ap_date_info:
        # these need to be reviewed later...
        obj['review_flag'] = True

        try:
            date_parts = [x.strip() for x in ap_date_info.split('-')]

            if len(date_parts) == 2:
                if "Before" in date_parts[0]:
                    obj['date_start_uncertain'] = True
                    date_parts[0] = date_parts[0].replace('Before', '').strip()

                if "Bef." in date_parts[0]:
                    obj['date_start_uncertain'] = True
                    date_parts[0] = date_parts[0].replace('Bef.', '').strip()

                if date_parts[0].isdigit():
                    obj['date_start'] = -int(date_parts[0])
                else:
                    obj['date_start_uncertain'] = True

                if date_parts[1].isdigit():
                    obj['date_end'] = -int(date_parts[1])
                else:
                    obj['date_end_uncertain'] = True

                if date_parts[0].isdigit() and date_parts[1].isdigit():
                    obj['review_flag'] = False

        except Exception as e:
            print 'FATAL ERROR saving extra date info ', post_year, ap_date_info, e.message

    return obj


def get_office_obj(office_name):
    """given a string, returns an office object"""

    # convert to lowercase
    office_name = office_name.lower()

    # tries to get the normalized office name from the
    try:
        oname = OFFICE_NAMES_DIC[office_name]
    except:
        print "WARNING: Unable to normalize office name: '%s'" %(office_name,)
        oname = office_name

    try:
        office = Office.objects.get(name=oname)
    except Office.DoesNotExist:

        # Adding new office
        #    in MRR all the offices are "civic" except for Vestal Virgin
        parent = Office.objects.get(name='Civic Offices')
        office = Office(name=oname, parent = parent)
        office.save()

        print 'Added Office: %s (id=%i)' % (office.name, office.id)

    return office


def run():
    #  for vol in ['mrr1', ]:
    for vol in ['mrr1', 'mrr2']:
        processXML(vol)

def processXML(volume):

    sdict = {
        'mrr1': ['Broughton MRR I', 'promrep/scripts/data/mrr1_all_MR_Officesv24.docx.html.xml'],
        'mrr2': ['Broughton MRR II', 'promrep/scripts/data/mrr2_converted_html_MRv12.xml']
    }

    source = SecondarySource.objects.get( abbrev_name = sdict[volume][0] )
    ifile = sdict[volume][1]

    print 'Will read', source, 'from file', ifile, '\n\n'

    page = file(ifile)
    soup = BeautifulSoup(page, features='xml')

    years = soup.findAll('year')

#    for year in years[70:71]:
    for year in years:
        year_str = year['name'].split()[0]
        print "\n\n>>>>> Year", year_str, years.index(year), '(',len(year.findAll('footnote')), 'footnotes)\n\n'

        # the footnotes can be added to a list
        # ... right at the "start" of the year
        fnote_dict = {}

        for fnote in year.findAll('footnote'):
            fnote_dict[fnote['ref']] = fnote

        # print fnote_dict

        # a post is defined by year and office
        for office_tag in year.findAll('office'):

            # removes the spaces from the office name
            office_name = office_tag['name'].strip()

            print ">>> Office:", office_name

            assertion_uncertain = False
            if "?" in office_name:
                # removes questionmark, marks assertion as uncertain
                office_name = office_name.strip('? ')
                assertion_uncertain = True

            # get office using office name
            office_obj = get_office_obj(office_name)

            #  every time a note is found, it is associated with all the post_assertions in the list
            person_ref_queue = []

            assertion = Post.objects.create(office=office_obj, date_info = year['name'].strip(), date_year = -int(year_str))

            # all these notes will be added to the individual PostAssertions
            assertion_notes_queue = []

            # all onotes are added to the PostAssertion objects in this assertion
            if len(office_tag.find_all('office-note')) > 0:
                for onote in office_tag.find_all('office-note'):
                    if onote.has_attr('name'):
                        a_note, created = PostAssertionNote.objects.get_or_create(
                                                text=onote['name'].strip(),
                                                secondary_source=source,
                                                note_type=PostAssertionNote.OFFICE_NOTE)

                        assertion_notes_queue.append(a_note)

            if office_tag.has_attr('footnote') or office_tag.has_attr('x_footnote'):
                if office_tag.has_attr('footnote'):
                    fnote_id = office_tag['footnote'].lstrip('#')
                else:
                    fnote_id = office_tag['x_footnote'].lstrip('#')

                if fnote_id in fnote_dict:
                    ofnote = fnote_dict[fnote_id]

                    afnote, created = PostAssertionNote.objects.get_or_create(
                                        text=ofnote.get_text().strip(),
                                        secondary_source=source,
                                        note_type=PostAssertionNote.OFFICE_FOOTNOTE)

                    assertion_notes_queue.append(afnote)
                else:
                    print "ERROR adding office fnote" + fnote_id

            # Post: Office + Year + Person
            for p in office_tag.find_all('person'):
                try:
                    name_str = p['name'].replace(u"’", "'").replace(u"\u2013", "-").replace(u'\xb4', "'")
                except Exception as e:
                    print "FATAL: Error getting person name", e

                print
                print "> Person:", name_str

                try:
                    # parses person from name
                    person_info = aux.parse_person(name_str)
                    # print 'pinfo->', person_info

                    if person_info is None:
                        # creates person with the whole name str as the nomen
                        person, created = Person.objects.get_or_create(nomen=name_str, review_flag=True)
                    else:
                        # removes the date_certainty info from the dictionary
                        if 'date_certainty' in person_info:
                            ap_date_info = person_info.pop('date_certainty').strip()
                        else:
                            ap_date_info = ""

                        if 'praenomen' in person_info:
                            try:
                                # creates the person object from the dictionary directly
                                person, created = Person.objects.get_or_create(
                                                                praenomen=person_info['praenomen'],
                                                                nomen=person_info['nomen'],
                                                                re_number=person_info['re_number'],
                                                                review_flag=False
                                                                )

                                if created:
                                    person.praenomen_uncertain = person_info.get('praenomen_uncertain', False)

                                    if 'patrician' in person_info:
                                        person.patrician = person_info['patrician']
                                        person.patrican_uncertain = person_info.get('patrician_uncertain', False)

                                    if '?' in person.nomen:
                                        person.nomen_uncertain = True

                                    if 'filiation' in person_info:
                                        person.filiation = person_info['filiation']
                                        if '?' in person_info['filiation']:
                                            person.filiation_uncertain = True

                                    if 'tribe' in person_info:
                                        person.tribe = person_info['tribe']

                                    if 'cognomen' in person_info:
                                        person.cognomen = person_info['cognomen']
                                        if '?' in person_info['cognomen']:
                                            person.cognomen_uncertain = True

                                    person.other_names = person_info.get('other_names', "")
                                    person.save()

                                else:
                                    print "Person already existed with id: ", person.id

                            except Exception as e:
                                print "FATAL ERROR (1) while creating person:", name_str, e.message

                        else:
                            try:
                                person = Person.objects.create(
                                            praenomen=Praenomen.objects.get(name='-'),
                                                    nomen=person_info['nomen'],
                                                    re_number=person_info['re_number'],
                                                    review_flag=True)
                            except Exception as e:
                                print "FATAL ERROR (2) while creating person:", name_str, e.message

                    # catch all ...
                    if person is None:
                        print "ERROR creating person-->", name_str

                    # creates the PostAssertion
                    else:
                        if p.has_attr('office-xref'):
                            oxref=p['office-xref']
                        else:
                            oxref=""

                        # TODO: stop creating repeated assertions
                        post_assertion, created = PostAssertion.objects.get_or_create(
                            role=RoleType.objects.get(name='Holder'),
                            post=assertion,
                            secondary_source=source,
                            person=person,
                            original_text = name_str,
                            office_xref = oxref
                        )

                        # PostAssertion Dates
                        ap_date_info = ap_date_info.strip("[:")
                        post_assertion.date_secondary_source = source

                        date_obj = parse_post_assertion_date(ap_date_info, year_str)
                        for key, value in date_obj.iteritems():
                            setattr(post_assertion, key, value)
                        post_assertion.save()

                        # Post Person uncertain
                        if p.has_attr('assertion-certainty') or (assertion_uncertain == True):
                            post_assertion.uncertain = True

                        # saves the order in the assertion
                        post_assertion.position = assertion.persons.count()
                        post_assertion.save()

                        # adds all assertion notes to the PostAssertion object
                        for assertion_note in assertion_notes_queue:
                            post_assertion.notes.add(assertion_note)

                        # add any footnotes the person might have
                        if p.has_attr('footnote') or p.has_attr('x_footnote'):
                            if p.has_attr('footnote'):
                                fnote_id = p['footnote'].lstrip('#')
                            else:
                                fnote_id = p['x_footnote'].lstrip('#')

                            if fnote_id in fnote_dict:
                                pnote = fnote_dict[fnote_id]
                                try:
                                    ap_fnote = PostAssertionNote(note_type = PostAssertionNote.FOOTNOTE, text = pnote.get_text().strip(), secondary_source=source)
                                    ap_fnote.save()
                                    post_assertion.notes.add(ap_fnote)
                                except:
                                    print "ERROR ADDING NOTES!!!"
                            else:
                                print "ERROR adding person footnote with id", fnote_id

                        # adds the post_assertion to the refs queue
                        person_ref_queue.append(post_assertion)

                        # if the next element is a reference
                        #   we're adding it to all the assertions in the assertion queue
                        if p.findNextSibling() == None:
                            pass
                        else:
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
                                note=PostAssertionNote.objects.create(
                                    text=ref_text.strip(),
                                    secondary_source=source)

                                notes_queue.append(note)

                                for fnote_id in footnotes:
                                    if fnote_id in fnote_dict:
                                        apfnote_obj = fnote_dict[fnote_id]
                                        apfnote = PostAssertionNote.objects.create(
                                                    note_type=PostAssertionNote.FOOTNOTE,
                                                    text=apfnote_obj.get_text().strip(),
                                                    secondary_source=source)
                                        notes_queue.append(apfnote)
                                    else:
                                        print "ERROR adding person footnote with id", fnote_id

                                for ap in person_ref_queue:

                                    for n in notes_queue:
                                        ap.notes.add(n)

                                # resets the ref queue
                                person_ref_queue = []


                except Exception as e:
                    print 'FATAL ERROR (3) parsing year ', year_str, p, e.message
