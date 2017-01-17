#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os

import parsing_aux as aux
from promrep.models import (Location, Person, PostAssertion, PostAssertionNote,
                            Praenomen, RoleType, SecondarySource, Tribe)


def run():
    for vol in ['mrr2_a2', 'mrr2_a3']:
        processCSV(vol)


def processCSV(volume):  # noqa

    sdict = {
        'mrr2_a2': ['Broughton MRR2 Appendix 2',
                    'promrep/scripts/data/MRRAppendix2v8.csv'],
        'mrr2_a3': ['Broughton MRR2 Appendix 3',
                    'promrep/scripts/data/MRRAppendix3v7.csv']
    }

    source = SecondarySource.objects.get(abbrev_name=sdict[volume][0])
    ifname = sdict[volume][1]

    print 'Will read', source, 'from file', ifname, '\n\n'

    log_fname = os.path.splitext(os.path.basename(ifname))[0] + '.log'

    ifile = open(ifname, 'rU')
    reader = csv.reader(ifile, delimiter=';', skipinitialspace=True)

    # skip header line
    reader.next()

    with open(log_fname, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(('original_name', 'created',
                             'person.id', 'post_assertion.id,' 'ap_note.id'))

        for original_row in reader:
            # Page  Review Later    Office  Revised Date Format Uncertain Date
            # Praenomen   Nomen   Filiation   Tribe   RE  Cognomen    Notes
            row = [a.strip() for a in original_row]

            (page, review_later, office_name, date_source_text, date_start,
             date_start_uncertain, date_end, date_end_uncertain,
             praenomen_str, nomen, filiation, tribe, re, cognomen,
             note_text) = row

            print("{}: {}-{}".format(office_name, date_start, date_end))

            post_assertion_uncertain = False
            if "?" in office_name:
                office_name = office_name.strip("?")
                post_assertion_uncertain = True

            location = False

            if "- Sicily" in office_name:
                office_name = office_name.strip("- Sicily")
                location, created = Location.objects.get_or_create(
                    name="Sicily", location_type=2)

            office_obj = aux.get_office_obj(office_name)

            if re:
                re_str = "(" + re + ")"
            else:
                re_str = ""

            original_name = " ".join(
                [x
                 for x
                 in [praenomen_str, nomen, filiation, tribe, re_str, cognomen]
                 if x])

            praenomen_uncertain = False

            try:
                if "?" in praenomen_str:
                    praenomen_str = praenomen_str.strip("?").strip()
                    praenomen_uncertain = True

                if praenomen_str == "" or praenomen_str == "-":
                    praenomen = Praenomen.objects.get(name="-")
                elif "." in praenomen_str:
                    praenomen = Praenomen.objects.get(abbrev=praenomen_str)
                else:
                    p_abbrev = praenomen_str + "."
                    praenomen = Praenomen.objects.get(abbrev=p_abbrev)

                person, created = Person.objects.get_or_create(
                    praenomen=praenomen,
                    nomen=nomen,
                    re_number=re,
                )

            except Exception as e:
                # cases where the praenomen does not exist
                # we'll simply create a new person without praenomen and
                # flagged for review

                person, created = Person.objects.get_or_create(
                    nomen=praenomen_str + " " + nomen,
                    re_number=re,
                    review_flag=True
                )

            # only updates fields if person was created
            if created:
                if praenomen_uncertain:
                    person.praenomen_uncertain = True

                person.cognomen = cognomen
                person.filiation = filiation

                if tribe:
                    try:
                        if "." not in tribe:
                            tribe_obj = Tribe.objects.get(abbrev=tribe + ".")
                            person.tribe = tribe_obj
                    except Exception as e:
                        print "ERROR getting tribe", tribe, e

                person.save()

            # creates the PostAssertion
            post_assertion = PostAssertion.objects.create(
                office=office_obj,
                role=RoleType.objects.get(name='Holder'),
                secondary_source=source,
                person=person,
                review_flag=review_later,
                date_source_text=date_source_text,
                date_start_uncertain=date_start_uncertain,
                date_end_uncertain=date_end_uncertain,
                original_text=original_name,
                uncertain=post_assertion_uncertain
            )

            if date_end:
                post_assertion.date_end = date_end
            if date_start:
                post_assertion.date_start = date_start
            if date_source_text:
                post_assertion.date_secondary_source = source
            if location:
                post_assertion.location = location

            post_assertion.save()

            if note_text:
                note_text = note_text.replace("**", ";").strip('"')
                ap_note = PostAssertionNote(
                    text=note_text, secondary_source=source)
                ap_note.save()
                post_assertion.notes.add(ap_note)

            spamwriter.writerow(
                (original_name,
                 created, person.id, post_assertion.id, ap_note.id))

    print "Wrote", log_fname
