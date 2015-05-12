#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
from promrep.models import Praenomen, Person, SecondarySource, PostAssertion, Office, Post, RoleType, Tribe, PostAssertionNote

import parsing_aux as aux
from promrep.scripts.offices_ref import OFFICE_NAMES_DIC

def run():
    ifile = open('promrep/scripts/data/MRRAppendix2v8.csv', 'rU')
    reader = csv.reader(ifile, delimiter=';', skipinitialspace=True)

    # skipt first line
    reader.next()

    total = 0
    found = 0

    source = SecondarySource.objects.get(abbrev_name="Broughton MRR2 Appendix 2")

    with open('mrr2_appendix_data.csv', 'wb') as csvfile:
        for original_row in reader:
            # Page  Review Later    Office  Revised Date Format Uncertain Date  Praenomen   Nomen   Filiation   Tribe   RE  Cognomen    Notes
            row = [a.strip() for a in original_row]

            (page, review_later, office_name, date_source_text, date_start,
             date_start_uncertain, date_end, date_end_uncertain,
             praenomen_str, nomen, filiation, tribe, re, cognomen, note_text) = row

            ##### print  praenomen_str, nomen, filiation, tribe, re, cognomen

            print office_name, date_start, date_end

            office_obj = aux.get_office_obj(office_name)

            # using the date_end as the date for posts
            # creating indivivual posts
            post = Post.objects.create(office=office_obj)
            if date_end:
                post.date_end = int(date_end)
                post.save()

            if re:
                re_str = "(" + re + ")"
            else:
                re_str = ""

            original_name = " ".join([x for x in [praenomen_str, nomen, filiation, tribe, re_str, cognomen] if x])
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
                    praenomen = Praenomen.objects.get(abbrev=p_abbrev )

                person, created = Person.objects.get_or_create(
                    praenomen=praenomen,
                    nomen=nomen,
                    re_number=re,
                )

            except Exception as e:
                # cases where the praenomen does not exist
                # we'll simply create a new person without praenomen and flagged for review

                person, created = Person.objects.get_or_create(
                    nomen = praenomen_str + " " + nomen,
                    re_number = re,
                    review_flag = True
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
                            tribe_obj = Tribe.objects.get(abbrev = tribe + ".")
                            person.tribe = tribe_obj
                    except Exception as e:
                        print "ERROR getting tribe", e

                person.save()

            # creates the PostAssertion
            post_assertion = PostAssertion.objects.create(
                role=RoleType.objects.get(name='Holder'),
                post=post,
                secondary_source=source,
                person=person,
                review_flag=review_later,
                date_source_text=date_source_text,
                date_start_uncertain=date_start_uncertain,
                date_end_uncertain=date_end_uncertain,
                original_text = original_name,
            )

            if date_end:
                post_assertion.date_end = date_end
            if date_start:
                post_assertion.date_start = date_start
            if date_source_text:
                post_assertion.date_secondary_source = source

            post_assertion.save()

            if note_text:
                ap_note = PostAssertionNote(text = note_text, secondary_source=source)
                ap_note.save()
                post_assertion.notes.add(ap_note)







