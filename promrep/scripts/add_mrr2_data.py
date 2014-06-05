#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, NavigableString
import regex

from promrep.models import Assertion, AssertionPerson, AssertionType, \
    Certainty, Date, DateType, Office, Person, Praenomen, \
    PrimarySource, RoleType, SecondarySource, Sex


def run():

    # this is the file exported by OpenOffice

    ifile = 'output-tidy-v4-MR-v1.xml'
    print 'Will process input file', ifile
    processXML(ifile)


def parse_person_name(self, text):

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
        (?P<affiliation>(%s|-)\s[fn-]?\.?\s){0,6}?
        (?P<cognomen>\(?[\?\w]+?\)?\s){0,8}
        (?<patrician>Pat\.\s)?
         \(\*?(?P<real>
             \d+                 | # either it's a number
             (RE\s)[\w\.]*?      | # or starts with RE
             \?                  | # or questino mark
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
        print captured.captures(1), captured.captures(2), \
            captured.captures(3)
        self.real = captured.captures('real')[0].strip()
        if len(captured.captures('praenomen')):
            self.praenomen = captured.captures('praenomen')[0].strip()
        self.nomen = captured.captures('nomen')[0].strip()
        if len(captured.captures('patrician')):
            self.is_patrician = True
        else:
            self.is_patrician = False
        cog_list = captured.captures('cognomen')
        if len(cog_list):
            self.cognomen_first = cog_list[0].strip()
        if len(cog_list) > 1:
            self.cognomen_other = \
                ' '.join(cog_list[1:]).strip().replace('  ', ' ')
        if len(captured.captures('date_certainty')):
            if captured.captures('date_certainty')[0].strip() == '?':
                self.date_certainty = 'Uncertain'
        self.affiliation = ''.join(captured.captures('affiliation'
                                   )).strip()
    else:
        print 'NADA'

def processXML(ifile):
    page = file(ifile)
    soup = BeautifulSoup(page, features='xml')

    years = soup.findAll('year')

    for year in years[0:4]:
        print year.find('name').get_text()

        for p in year.find_all('person'):
            text = p.find('name').get_text()

            parse_person_name(text)
