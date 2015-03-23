#!/usr/bin/python
# -*- coding: utf-8 -*-

from promrep.models import Assertion
import collections

def run():
    # nom_list = [p.cognomen for p in Person.objects.all()]
    # counter=collections.Counter(nom_list)
#
    # for name, freq in counter.most_common():
    #     print "%s,\t%s" %(freq, name)

    for a in Assertion.objects.all():
        for ap in a.assertionperson_set.all():
            print ap.original_text