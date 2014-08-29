#!/usr/bin/python
# -*- coding: utf-8 -*-

# data import auxiliary functions

from django.db import transaction
from promrep.models import Assertion, AssertionPerson, \
    Date, DateType, Office, Person, Praenomen, \
    PrimarySource, SecondarySource, Sex

import regex
import logging

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


def parse_person(text):
    """Will return a person object or None if unable to parse the person"""

    logger.info("ParsePersonName: %s" %(text))

    praenomen_list = [regex.escape(p.abbrev) for p in Praenomen.objects.all()]
    praenomen_list.append(regex.escape('-'))
    praenomen_abbrev = r'(?:%s)' % '|'.join(praenomen_list)

    person_re = \
        regex.compile(r"""^
        (?P<date_certainty>
            \?[\s\-]    | # question mark followed by either a space or a dash in the start of line
            .*?\:\s     | # or something followed by colon AND space
            )?
        (?P<praenomen>%s\??\s)?
        (?P<nomen>\(?\w+?\)?\s)?
        (?P<filiation>%s\s[fn-]?\.?\s){0,6}
        (?P<cognomen>\(?[\?\w]+?\.?\)?\s){0,8}?
        (?<patrician>Pat\.{1,2}\??\s)? # outlier cases w/ 2 dots...
         \((?P<real>
            \*?         # can have an asterisk followed by...
                [\d\.]+?            | # either a number or cases like (*2.100)
                (RE\s)[\w\.]*?      | # or starts with RE
                \?                  | # or question mark
                [A-Z\d\.]+?         | # or uppercase letters with numbers and dots (no spaces)
                [\d]+,\s\w+\.?\s\d+ | # or cases like (14, Supb. 6)
                not\sin\sRE           # or says "not in RE"
         )\)
         .*                         # in parenthesis (can have an asterisk)
         """
                       % (praenomen_abbrev, praenomen_abbrev),
                      regex.VERBOSE)

    captured = person_re.match(text)

    if captured:

        real = captured.captures('real')[0].strip()
        sex = Sex.objects.get(name='Male')

        praen_cert = True
        if len(captured.captures('praenomen')):
            praenomen_str = captured.captures('praenomen')[0].strip()

            if "?" in praenomen_str:
                praen_cert = False
                praenomen_str = praenomen_str.replace("?", "")

            praenomen = Praenomen.objects.get(abbrev=praenomen_str)

        else:
            praenomen = None

        nomen = captured.captures('nomen')[0].strip()

        # parse patrician and patrician certainty

        pat_str = captured.captures('patrician')
        pat_certain = True
        is_pat = False

        if len(pat_str):
            if "?" in pat_str[0]:
                pat_certain = False
            is_pat = True

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
                    praenomen_certainty = praen_cert,
                    filiation=filiation,
                    cognomen=cognomen_first,
                    other_names=other_names,
                    patrician=is_pat,
                    patrician_certainty=pat_certain,
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
