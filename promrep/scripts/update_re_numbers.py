import csv

from promrep.models import Praenomen, Person

def run():
    # U flag: universal new-line mode
    ifile = open('promrep/scripts/data/OldRENumbersv3.csv', 'rU')
    reader = csv.reader(ifile, delimiter=',', skipinitialspace=True)

    # next(reader, None)

    total = 0
    found = 0

    for original_row in reader:
        total = total + 1
        row = [a.strip() for a in original_row]
        (praenomen_str, nomen, re, new_re) = row

        try:
            if praenomen_str == "":
                praenomen = Praenomen.objects.get(name="-")
            elif "." in praenomen_str:
                praenomen = Praenomen.objects.get(abbrev=praenomen_str)
            else:
                praenomen = Praenomen.objects.get(name=praenomen_str)

            p = Person.objects.filter(praenomen=praenomen, nomen=nomen, re_number=re)

            if len(p) == 1:
                found = found + 1
                print p[0].id, praenomen_str, nomen, re
            elif len(p) > 1:
                print 'ERROR: More than one person found:', praenomen_str, nomen, re
            else:
                print 'ERROR: Unable to find person:', praenomen.abbrev(), nomen, re

        except:
            print 'ERROR: Praenomen lookup error:', praenomen_str, nomen, re

    print total, found