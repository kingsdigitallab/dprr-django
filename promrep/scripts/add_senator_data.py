# -*- coding: utf-8 -*-

from promrep.models import (
    Office
)


def run():
    print("Adding Senator Status Assertions")

    add_simple_senators()


# This process affects each person who has a post assertion with a start
# date after -180, for the following offices - quaestor, tribunis plebis,
# aedilis (and subtypes), praetor (and subtypes), consul (and subtypes),
# censor (and subtypes), princeps senatus and senator including the
# different subtypes - senator quaestorius, praetorius consularis etc)

# If a person has post assertion as listed above except senator and its
# subtypes, then create a senator status assertion

def add_simple_senators():

    office_list = ['quaestor', 'tribunus plebis', 'aedilis',
                   'praetor', 'consul', 'censor', 'princeps senatus',
                   'senator']

    all_offices = office_list

    for oname in office_list:
        print oname
        off = Office.objects.get(name=oname)
        all_offices += list(off.get_descendants())

    print all_offices
    print len(all_offices)
