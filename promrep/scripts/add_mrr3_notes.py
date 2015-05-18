#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os
from promrep.models import SecondarySource, PostAssertionNote
import codecs

def run():

    note_files = [ 'promrep/scripts/data/MRR3ShortNotesV2.csv',
                   'promrep/scripts/data/MRR3LongNotesV2.csv']

    source = SecondarySource.objects.get( abbrev_name = 'Broughton MRR3' )

    for ifname in note_files:
        print 'Will read notes from file', ifname, '\n\n'

        ifile = codecs.open(ifname, 'r', encoding='latin1')
        log_fname = os.path.splitext(os.path.basename(ifname))[0] + '.log'

        with open(log_fname, 'wb') as log_file:
            spamwriter = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(('id', 'note'))

            for i, line in enumerate(ifile):

                note_text = line.encode('utf-8').replace("**", ";").strip('"')

                print str(i) + ":" , note_text

                note = PostAssertionNote.objects.create(text=note_text, secondary_source=source)
                spamwriter.writerow((note.id, note_text[0:20]))