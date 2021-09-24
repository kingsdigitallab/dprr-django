#!/usr/bin/python
# -*- coding: utf-8 -*-

# data import auxiliary functions
import logging

import regex
from promrep.models import Office, Person, Praenomen, Sex, Tribe
from promrep.scripts.offices_ref import OFFICE_NAMES_DIC

# TODO: configure in settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# add a file handler
fh = logging.FileHandler('data_import.log')
fh.setLevel(logging.DEBUG)
# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(frmt)
# add the Handler to the logger
logger.addHandler(fh)


def parse_person(text):  # noqa
    """ Will return a dictionary with all the parsed attributes"""

    # returnable dictionary
    person_data = {}

    praenomen_list = [regex.escape(p.abbrev) for p in Praenomen.objects.all()]
    praenomen_abbrev = r'(?:%s)' % '|'.join(praenomen_list)
    full_prae_list = [regex.escape(p.name) for p in Praenomen.objects.all()]
    praenomen_full = r'(?:%s)' % '|'.join(full_prae_list)

    tribe_list = [regex.escape(t.abbrev) for t in Tribe.objects.all()]
    tribe_abbrev = r'(?:%s)' % '|'.join(tribe_list)

    person_re = \
        regex.compile(r"""^
        ([abc123]\.\s)?    # TODO: what to do with these???
        (?P<date_certainty>
            \[?\?[\s\-]     |   # question mark followed by a space or a dash
                                # in the start of line
            .*?\:\s         |   # or something followed by colon AND space
            \? | # or question mark...
            )?
        (?P<praenomen>
         %s\??\s |
         \(%s\)\s |
         %s\??\s
         )?
        (\?\s)? # TODO - question mark after praenomen??...
        (?P<nomen>\(?\w+?\)?\s)?
        (\?\s)? # TODO - question mark after nomen??...
        (?P<filiation>%s\s[fn-]?\.?\s |
         \(?[-\w]+[\.\)]?(\s\?)?\sf.\s[-\w]+[\.\)]?\sn.\)?\s |
         \(?[-\w]+[\.\)]?(\s\?)?\sf.\)?\s |
         \(?[-\w]+[\.\)]?\sn.\)?\s
         ){0,6}
        (?P<tribe>%s\s)?               # only one tribe abbrev
        (?P<cognomen>\(?[\?\w-]+?\)?\s){0,8}?
        (?P<patrician>Pat\.{1,2}\s?\??\s)? # outliers: 1/2 dots, space?
         \((?P<real>
            \*?         # can have an asterisk followed by...
                [\d\. \?]+?            | # either a number or cases
                                         # like (*2.100)
                (RE\s)[\w\.]*?         | # or starts with RE
                \?                     | # or question mark
                (\*?\d+,?\s?){1,8}     | # or 2 or more numbers
                [A-Z\d\.]+?            | # or uppercase letters with numbers
                                         # and dots (no spaces)
                [\d]+,\s(cf.\s)?\w+\.?\s\d+ | # or cases like (14, Supb. 6)
                (\d+\s,\s)?cf.\s?\d+        | # or cases like (cf. 92)
                # or cases like (46a, Supb. 5.356ff.)
                [\d]+[a-z]*?,( RE)?\s[\d\w]*?\.\s?\d+?\.?\d*?\w*?\.? |
                # or cases like (88, cf. Supb. 1.271)
                [\d]+[a-z]*?,\scf\.\s\w+\.\s\d+\.\d+ |
                \w+\.?\s\*?\d+ | # or cases like Veturius *18, or Cin. *1
                \d+?\sand\s\d+? |
                not\sin\s\*?RE  |         # or says "not in RE"
                RE.*
         )\)
         .*                         # in parenthesis (can have an asterisk)
         """
                      % (praenomen_abbrev, praenomen_abbrev,
                         praenomen_full, praenomen_abbrev, tribe_abbrev),
                      regex.VERBOSE)

    captured = person_re.match(text)

    try:
        real = captured.captures('real')[0].strip()
        person_data['re_number'] = real

        # TODO: what to do with the empty praenomen??
        if len(captured.captures('praenomen')):
            praenomen_str = captured.captures('praenomen')[0].strip()

            # TODO:
            praenomen_str = praenomen_str.strip("()")

            if "?" in praenomen_str:
                person_data['praenomen_uncertain'] = True
                praenomen_str = praenomen_str.replace("?", "")

            try:
                if praenomen_str == "-.":
                    praenomen = Praenomen.objects.get(name="-")
                elif "." in praenomen_str:
                    praenomen = Praenomen.objects.get(abbrev=praenomen_str)
                else:
                    praenomen = Praenomen.objects.get(name=praenomen_str)
            except:
                logger.error(
                    'ERROR: Praenomen lookup error: %s', praenomen_str)
                return None

            person_data['praenomen'] = praenomen

        nomen = captured.captures('nomen')[0].strip()
        person_data['nomen'] = nomen.strip("?()[]")

        # parse patrician and patrician certainty
        pat_str = captured.captures('patrician')

        if len(pat_str):
            person_data['patrician'] = True

            if "?" in pat_str[0]:
                person_data['patrician_uncertain'] = True

        if len(captured.captures('tribe')):
            tribe_abbrev = captured.captures('tribe')[0].strip()
            tribe = Tribe.objects.get(abbrev=tribe_abbrev)
            person_data['tribe'] = tribe

        cog_list = captured.captures('cognomen')

        if len(cog_list):
            cognomen_first = cog_list[0].strip()
            person_data['cognomen'] = cognomen_first

        if len(cog_list) > 1:
            other_names = ' '.join(cog_list[1:]).strip().replace('  ', ' ')
            person_data['other_names'] = other_names

        if 'cognomen' and 'other_names' in person_data:
            if person_data['other_names'] == "?)" and \
                    person_data['cognomen'][0] == "(":
                person_data['cognomen'] = person_data['cognomen'] + " ?)"
                person_data.pop('other_names')

        if len(captured.captures('date_certainty')):
            person_data['date_certainty'] = \
                captured.captures('date_certainty')[0].strip()

        person_data['filiation'] = ''.join(
            captured.captures('filiation')).strip()

        return person_data

    except:
        print 'Unable to parse the name:', text
        return None


def parse_brennan_person(text):  # noqa
    """Will return a person object or None if unable to parse the person"""

    praenomen_list = [regex.escape(p.abbrev) for p in Praenomen.objects.all()]
    praenomen_abbrev = r'(?:%s)' % '|'.join(praenomen_list)

    tribe_list = [regex.escape(t.abbrev) for t in Tribe.objects.all()]
    tribe_abbrev = r'(?:%s)' % '|'.join(tribe_list)

    person_re = \
        regex.compile(r"""^
        (?P<praenomen>%s\??\s)?
        (?P<nomen>\(?[A-Z][a-z]{2,20}\)?)
        \s?
        (?P<patrician>Pat\.\??\s)?
        (\((?P<real>
            \*?                       # can have an asterisk followed by...
                \d*?,?/?\s?\d*?                           | # (14, 6), 148/149
                [\d\.]+?       | # either a number or cases like (*2.100)
                (RE\s)[\w\.]*? | # or starts with RE
                \?             | # or question mark
                [A-Z\d\.]+?    | # or uppercase letters with numbers and dots
                                 # (no spaces)
                [\d]+,\s\w+\.?\s\d+                     | # or (14, Supb. 6)
                [A-Z][a-z]+\.?\s\*?\d*                  | # or  Cin. *12
                [A-Z][a-z]+\s\d*\s\=\s[A-Z][a-z]+\s\d*  | # or cases like
                                                    # or Atilius 16 = Acilius 7
                not\sin\sRE           # or says "not in RE"
        )\)\s*)?
        (?P<filiation>%s\s[fn-]?\.?\s){0,6}
        (?P<tribe>%s\s)?
        (?P<cognomen>.*)?
         """
                      % (praenomen_abbrev, praenomen_abbrev, tribe_abbrev),
                      regex.VERBOSE)

    captured = person_re.match(text)

    # print text
    # print captured.groups()

    if captured is None:
        logger.error('Unable to parse the person: %s' % (text))
        return None

    if len(captured.captures('real')):
        real = captured.captures('real')[0].strip()
    else:
        real = ""
    sex = Sex.objects.get(name='Male')

    praen_cert = False
    if len(captured.captures('praenomen')):
        praenomen_str = captured.captures('praenomen')[0].strip()

        if "?" in praenomen_str:
            praen_cert = True
            praenomen_str = praenomen_str.replace("?", "")

        try:
            praenomen = Praenomen.objects.get(abbrev=praenomen_str)
        except:
            logger.error('Praenomen lookup error: %s', praenomen_str)
            return None

    else:
        praenomen = None

    nomen = captured.captures('nomen')[0].strip()

    # parse patrician and patrician certainty

    pat_str = captured.captures('patrician')
    pat_uncertain = False
    is_pat = False

    if len(pat_str):
        if "?" in pat_str[0]:
            pat_uncertain = True
        is_pat = True

    # tribe = None
    # if len(captured.captures('tribe')):
    #     tribe_abbrev = captured.captures('tribe')[0].strip()
    #     tribe = Tribe.objects.get(abbrev=tribe_abbrev)

    cog_list = captured.captures('cognomen')[0].strip().split(' ')

    cognomen_first = ''
    other_names = ''

    if len(cog_list):
        cognomen_first = cog_list[0].strip()

    if len(cog_list) > 1:
        other_names = ' '.join(cog_list[1:]).strip().replace('  ', ' ')

    # if len(captured.captures('date_certainty')):
    #    if captured.captures('date_certainty')[0].strip() == '?':
    #        person.date_certainty = 'Uncertain'

    filiation = ''.join(captured.captures('filiation')).strip()

    # TODO: chars to be stripped from the nomen when saving to the database...
    # these chars indicate uncertainty, etc...

    try:
        # TODO: add tribe object separately
        person = Person(
            sex=sex,
            praenomen=praenomen,
            nomen=nomen.strip("?()[]"),
            praenomen_uncertain=praen_cert,
            filiation=filiation,
            cognomen=cognomen_first,
            re_number=real,
            other_names=other_names,
            patrician=is_pat,
            patrician_uncertain=pat_uncertain,
        )

    except Exception as e:
        print 'Failed to create person %s (%s)' % (e.message, type(e))
        return None

    return person


def get_office_obj(office_name):
    """given a string, returns an office object"""

    # convert to lowercase
    office_name = office_name.lower()

    # tries to get the normalized office name from the
    try:
        oname = OFFICE_NAMES_DIC[office_name]
    except:
        oname = office_name

    try:
        office = Office.objects.get(name=oname)
    except Office.DoesNotExist:

        # Adding new office
        #    in MRR all the offices are "civic" except for Vestal Virgin
        parent = Office.objects.get(name='Civic Offices')
        office = Office(name=oname, parent=parent)
        office.save()

        print 'Added Office: %s (id=%i)' % (office.name, office.id)

    return office
