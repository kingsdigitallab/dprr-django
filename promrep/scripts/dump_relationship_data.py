import csv
import itertools
import logging
from os import path

from django.db.models import Q

from promrep.models import Person, RelationshipAssertion, Praenomen, \
    SecondarySource, PrimarySource, Sex, RelationshipType, \
    RelationshipAssertionPrimarySource


def print_relationship(rel):
    print '{}; {}; {}; {}; {}'.format(rel.person.id, rel.person, rel.relationship, rel.related_person.id, rel.related_person, )


def dump_all():
    for p in Person.objects.all():
        print_rels(p)


def dump_rels(person, relationships=[], visited=[]):

    if person in visited:
        return relationships

    visited.append(person)

    d_rels = list(RelationshipAssertion.objects.filter(person=person))
    i_rels = list(RelationshipAssertion.objects.filter(related_person=person))

    if not d_rels and not i_rels:
        return relationships

    if d_rels:
        relationships += d_rels
    if i_rels:
        relationships += i_rels

    for rel in d_rels:
        dump_rels(rel.related_person, relationships, visited)

    for rel in i_rels:
        dump_rels(rel.person, relationships, visited)

    return relationships


def run():
    seed = 2597

    all_rels = set(dump_rels(Person.objects.get(id=seed)))

#    persons = dump_person_rels(seed)

#    all_rels = RelationshipAssertion.objects.filter(
#        Q(person__id__in=persons) | Q(related_person__id__in=persons))

    print "rel.person.id; rel.person; rel.relationship; rel.related_person.id; rel.related_person"
    for rel in all_rels:
        # print rel
        print_relationship(rel)
