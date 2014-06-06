#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import regex

from promrep.models import Assertion, AssertionPerson, AssertionType, \
    Certainty, Date, DateType, Office, Person, Praenomen, \
    PrimarySource, RoleType, SecondarySource, Sex


def run():

    # this is the file exported by OpenOffice

    ifile = 'promrep/scripts/data/output-tidy-v4-MR-v1.xml'
    print 'Will process input file', ifile
    processXML(ifile)


def parse_person_name(text):

    print 'Will parse person: ', text

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
        real = captured.captures('real')[0].strip()

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
        cognomen_other = ''

        if len(cog_list):
            cognomen_first = cog_list[0].strip()

        if len(cog_list) > 1:
            cognomen_other = ' '.join(cog_list[1:]).strip().replace('  '
                    , ' ')

        # if len(captured.captures('date_certainty')):
        #    if captured.captures('date_certainty')[0].strip() == '?':
        #        person.date_certainty = 'Uncertain'

        filiation = ''.join(captured.captures('filiation')).strip()

        p = Person(
            original_text=text,
            sex=sex,
            real_number=real,
            nomen=nomen,
            praenomen=praenomen,
            filiation=filiation,
            cognomen_first=cognomen_first,
            cognomen_other=cognomen_other,
            is_patrician=is_patrician,
            )

        try:
            p.save()
            print '      [OK] Saved person ' + str(p) + ' with id: ' \
                + str(p.id)
        except Exception, e:
            raise e
    else:

        print '[ERROR] Could not parse the person:', text


def processXML(ifile):
    page = file(ifile)
    soup = BeautifulSoup(page, features='xml')

    years = soup.findAll('year')

    for year in years[0:4]:
        print 'YEAR ' + year.find('name').get_text()

        for office_tag in year.findAll('office'):
            office_name = office_tag.find('name').get_text()
            print '[mrr2-add]: Processing OFFICE ' + office_name

            try:
                office = Office.objects.get(name=office_name)
                print 'Found', office
            except Office.DoesNotExist:

                # in MRR2 all offices are "civil"

                parent = Office.objects.get(name='Civic Offices')

                office = Office(name=office_name)
                office.parent = parent
                office.save()

                print 'Added ', office, office.id

            for p in office_tag.find_all('person'):
                text = p.find('name').get_text()
                print 'PERSON ' + text


                # parse_person_name(text)
