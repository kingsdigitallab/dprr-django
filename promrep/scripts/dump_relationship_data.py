from promrep.models import Person, RelationshipAssertion

try:
    import simplejson as json
except:
    import json


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


def person_rel_json(person):
    rels, persons = dump_rels(person, [], [])

    edges = []
    nodes = []

    for rel in rels:
        rel_dict_el = {
            "id": rel.id,
            "source": rel.person.id,
            "target": rel.related_person.id,
            "label": rel.relationship.__unicode__()}

        if rel_dict_el not in edges:
            edges.append(rel_dict_el)

    for person in persons:
        p_el_dict = {
            "id": person.id,
            "label": person.__unicode__()
        }

        if p_el_dict not in nodes:
            nodes.append(p_el_dict)

    return json.dumps({"edges": edges, "nodes": nodes})


def run():

    rel_json = person_rel_json(Person.objects.get(id=1452))
    print rel_json

    # visited_persons = set()

    # for p in Person.objects.filter(id=4172):
    # for p in Person.objects.all():
    #     print p.id
#
    #     if p.id not in visited_persons:
    #         visited_persons.add(p.id)
    #         p_rels, visited = dump_rels(p, [], [])
#
    #         for pers in visited:
    #             visited_persons.add(pers.id)
#
    #         p_rels = set(p_rels)
#
    #         if len(p_rels) > 0:
#
    #             fname = "rel_csv/" + str(p.id) + ".csv"
#
    #             with open(fname, 'wb') as csvfile:
    #                 spamwriter = csv.writer(
    #                     csvfile, delimiter=';', quotechar='"',
    #                        quoting=csv.QUOTE_MINIMAL)
    #                 spamwriter.writerow(
    #                     ["person1 ID", "person1",
    #                      "relationship", "person2 ID", "person2"])
    #
    #                 for rel in p_rels:
    #                     spamwriter.writerow(
    #                         [rel.person.id, rel.person,
    # rel.relationship, rel.related_person.id, rel.related_person])
#
    #             csvfile.close()
    #             print "Wrote {}".format(fname)
#
    #         else:
    #             print "No rels found for person {}".format(p.id)
#
    #     else:
    #         print "Skipping... {}".format(p.id)
