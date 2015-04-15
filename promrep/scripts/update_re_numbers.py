import csv

from promrep.models import Praenomen, Person

def run():
    # U flag: universal new-line mode
    ifile = open('promrep/scripts/data/OldRENumbersv6.csv', 'rU')
    reader = csv.reader(ifile, delimiter=',', skipinitialspace=True)

    total = 0
    found = 0

    with open('re_update_log.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

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

                if len(p) == 0:
                    raise ValueError('No person found!')
                elif len(p) > 1:
                    raise ValueError('More than one person found!')

                person = p[0]
                found = found + 1

                person.re_number_old = re
                person.re_number = new_re

                person.save()
                spamwriter.writerow((praenomen_str, nomen, re, new_re, person.id))

            except Exception as e:
                spamwriter.writerow((praenomen_str, nomen, re, new_re, "ERROR: " + e.message))
                print 'ERROR:', e, praenomen_str, nomen, re

        print total, found