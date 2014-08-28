#!/usr/bin/python
# -*- coding: utf-8 -*-

# data import auxiliary functions

from django.db import transaction
from promrep.models import Assertion, AssertionPerson, \
    Date, DateType, Office, Person, Praenomen, \
    PrimarySource, SecondarySource, Sex

import regex

def person_exists(person):
    """Returns False if the person doesn't exist, None if there are more than one or id if it exists"""

    # tests if there are more persons with the same identifier (nomen + real)
    identic = \
        Person.objects.filter(real_number=person.real_number,
                              nomen=person.nomen)

    if identic.count() == 1:
        existing_person = identic[0]
        # should print the debug information
        diffs = existing_person.compare(person)
        print "[SAME_PERSON] Parsing person already in database:",

        diff_keys = diffs[0].keys()
        if len(diff_keys) == 0:
            print "No new info."
        else:
            print "printing diffs:"

        for key in diff_keys:
            print '[SAME_PERSON]', key, 'Old:', diffs[0][key], 'New:', diffs[1][key]

        print '[SAME_PERSON] Keeping previous (id=' + str(existing_person.id)  + ') in database... '

        return existing_person.id

    elif identic.count() > 1:
        # todo: print a verbose error
        print '[ERROR] More than one person matches query... not adding person to db.'
        return None
    else:
        return False


def parse_person_name(text):
    """Will return a person object or None if unable to parse the person"""

    print
    print '[DEBUG] Will parse person: ', text

    # TODO: this should come from the database...

    praenomen_list = [
        'Agr\.',
        'Ap\.',
        'A\.',
        'K\.',
        'D\.',
        'F\.',
        'C\.',
        'Cn\.',
        'Hostus',
        'Lars',
        'L\.',
        'Mam\.',
        "M'\.",
        'M\.',
        'N\.',
        'Oct\.',
        'Opet\.',
        'Pacuvius',
        'Post\.',
        'Proc\.',
        'P\.',
        'Q\.',
        'Ser\.',
        'Sex\.',
        'Sp\.',
        'St\.',
        'Ti\.',
        'T\.',
        '\?',
        'V\.',
        'Vol\.',
        'Vop\.',
        ]
    praenomen_abbrev = r'(?:%s)' % '|'.join(praenomen_list)

    person_re = \
        regex.compile(r"""^
        (?P<date_certainty>\?[\s\-])?    # question mark followed by either a space or a dash in the start of line
        (?P<praenomen>%s\s)?
        (?P<nomen>\(?\w+?\)?\s)?
        (?P<filiation>(%s|-)\s[fn-]?\.?\s){0,6}?
        (?P<cognomen>\(?[\?\w]+?\)?\s){0,8}
        (?<patrician>Pat\.\s)?
         \((?P<real>
            \*?
             \d+?                 | # either it's a number
             (RE\s)[\w\.]*?      | # or starts with RE
             \?                  | # or question mark
             [A-Z\d\.]+?         | # or uppercase letters with numbers and dots (no spaces)
             [\d]+,\s\w+\.?\s\d+ | # or cases like (14, Supb. 6)
             not\sin\sRE                # or says "not in RE"
         )\)
         .*                         # in parenthesis (can have an asterisk)
         """
                       % (praenomen_abbrev, praenomen_abbrev),
                      regex.VERBOSE)

    captured = person_re.match(text)

    if captured:

        real = captured.captures('real')[0].strip()
        print real
        sex = Sex.objects.get(name='Male')

        if len(captured.captures('praenomen')):
            praenomen = captured.captures('praenomen')[0].strip()
            praenomen = Praenomen.objects.get(abbrev=praenomen)
        else:
            praenomen = None

        nomen = captured.captures('nomen')[0].strip()

        if len(captured.captures('patrician')):
            is_patrician = True
        else:
            is_patrician = False

        cog_list = captured.captures('cognomen')

        cognomen_first = ''
        other_names = ''

        if len(cog_list):
            cognomen_first = cog_list[0].strip()

        if len(cog_list) > 1:
            other_names = ' '.join(cog_list[1:]).strip().replace('  '
                    , ' ')

        # if len(captured.captures('date_certainty')):
        #    if captured.captures('date_certainty')[0].strip() == '?':
        #        person.date_certainty = 'Uncertain'

        filiation = ''.join(captured.captures('filiation')).strip()

        try:
            with transaction.atomic():
                person = Person(
                    sex=sex,
                    real_number=real,
                    nomen=nomen,
                    praenomen=praenomen,
                    filiation=filiation,
                    cognomen=cognomen_first,
                    other_names=other_names,
                    patrician=is_patrician,
                    )

                if person:
                    print "Added " + person.get_name()
                else:
                    print "Failed to add " + text

            return person

        except Exception as e:
            print '%s (%s)' % (e.message, type(e))


    else:
        print '[ERROR] Could not parse the person:', text
        return None
