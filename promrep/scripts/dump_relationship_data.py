import csv
import itertools
import logging
from os import path

from django.db.models import Q

from promrep.models import Person, RelationshipAssertion, Praenomen, \
    SecondarySource, PrimarySource, Sex, RelationshipType, RelationshipAssertionPrimarySource


def dump_rels(person, relationships=[], visited=[]):
    """Recursive function that given a person returns two lists
    relationships - list of relationships linked to that person
    visited - list of persons linked to that person via relationships
    """

    if person in visited:
        return relationships, visited

    visited.append(person)

    d_rels = list(RelationshipAssertion.objects.filter(person=person))
    i_rels = list(RelationshipAssertion.objects.filter(related_person=person))

    if not d_rels and not i_rels:
        return relationships, visited

    if d_rels:
        relationships += d_rels
    if i_rels:
        relationships += i_rels

    for rel in d_rels:
        dump_rels(rel.related_person, relationships, visited)

    for rel in i_rels:
        dump_rels(rel.person, relationships, visited)

    return relationships, visited


def run():
    visited_persons = set()

    # for p in Person.objects.filter(id=4172):
    for p in Person.objects.all():
        print p.id

        if p.id not in visited_persons:
            visited_persons.add(p.id)
            p_rels, visited = dump_rels(p, [], [])

            for pers in visited:
                visited_persons.add(pers.id)

            p_rels = set(p_rels)

            if len(p_rels) > 0:

                fname = "rel_csv/" + str(p.id) + ".csv"

                with open(fname, 'wb') as csvfile:
                    spamwriter = csv.writer(
                        csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow(
                        ["person1 ID", "person1", "relationship", "person2 ID", "person2"])

                    for rel in p_rels:
                        spamwriter.writerow(
                            [rel.person.id, rel.person, rel.relationship, rel.related_person.id, rel.related_person])

                csvfile.close()
                print "Wrote {}".format(fname)

            else:
                print "No rels found for person {}".format(p.id)

        else:
            print "Skipping... {}".format(p.id)
