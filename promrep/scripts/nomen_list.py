#!/usr/bin/python
# -*- coding: utf-8 -*-

from promrep.models import Post


def run():
    # nom_list = [p.cognomen for p in Person.objects.all()]
    # counter=collections.Counter(nom_list)
    #
    # for name, freq in counter.most_common():
    #     print "%s,\t%s" %(freq, name)

    for a in Post.objects.all():
        for ap in a.PostAssertion_set.all():
            if ap.secondary_source.id == 1:
                print ap.original_text
