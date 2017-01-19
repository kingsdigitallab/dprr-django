from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import logging
from promrep.models import Person, RelationshipAssertion, RelationshipType
from django.db.models import Q
import csv
import datetime


# EHall 19/1/2017

class Command(BaseCommand):
    args = '<page document_path document_path ...>'
    help = 'Adds inverse relationships if they do no exist'

    logger = logging.getLogger(__name__)

    def findfromsiblings(self, person, sibs, relationship, single):
        relationships = []
        for sib in sibs:
            try:
                found = RelationshipAssertion.objects.get(related_person=sib.related_person,
                                                          relationship=relationship)
            except ObjectDoesNotExist:
                pass
            if found is not None:
                relationships.append(
                    RelationshipAssertion(extra_info="Inferred", person=person, related_person=found.person,
                                          relationship=relationship))
                if single:
                    break
        return relationships

    # Populate inferred family relationships based on rules in DPRR-257
    # IMPORTANT NOTE: Assumes inverse relationships already populated
    def add_inferred_relationships(self):
        new_rels = []
        type_mother = RelationshipType.objects.get(name="mother of")
        type_father = RelationshipType.objects.get(name="father of")
        type_son = RelationshipType.objects.get(name="son of")
        type_daughter = RelationshipType.objects.get(name="daughter of")

        for person in Person.objects.all():
            sibs = []
            children = []
            mother = None
            father = None
            spouse = None
            # Sort relationships into family members
            for relassert in RelationshipAssertion.objects.all(person=person):
                # Mother/Father
                if relassert.relationship.name == "father of" or relassert.relationship.name == "mother of":
                    children.append(relassert)
                elif relassert.relationship.name == "son of" or relassert.relationship.name == "daughter of":
                    # Son/Daughter
                    if relassert.related_person.sex.name == "Male":
                        father = relassert
                    else:
                        mother = relassert
                elif relassert.relationship.name == "brother of" or relassert.relationship.name == "sister of":
                    sibs.append(relassert)
                elif relassert.relationship.name == "married to":
                    spouse = relassert

            # Check for father and mother
            if father == None and len(sibs) > 0:
                finds = self.findfromsiblings(person, sibs, RelationshipType.objects.get("father of"), True)
                if len(finds) > 0:
                    # TODO save father
                    father = finds[0]
                    new_rels.append(father)
            if mother == None and len(sibs) > 0:
                finds = self.findfromsiblings(person, sibs, RelationshipType.objects.get("mother of"), True)
                if len(finds) > 0:
                    # TODO save
                    mother = finds[0]
                    new_rels.append(mother)

            # Go through siblings and make sure their parent records are complete
            for sib in sibs:
                if mother != None and RelationshipAssertion.objects.filter(related_person=sib.related_person,
                                                                           relationship__name="mother of").count() == 0:
                    new_rels.append(
                        RelationshipAssertion(extra_info="Inferred", related_person=sib.related_person,
                                              person=mother.related_person,
                                              relationship=mother.relationship))
                    new_rels.append(
                        RelationshipAssertion(extra_info="Inferred", person=sib.related_person,
                                              related_person=mother.related_person,
                                              relationship=mother.get_inverse_relationship()))
                if father != None and RelationshipAssertion.objects.filter(related_person=sib.related_person,
                                                                           relationship__name="father of").count() == 0:
                    new_rels.append(
                        RelationshipAssertion(extra_info="Inferred", related_person=sib.related_person,
                                              person=father.related_person,
                                              relationship=father.relationship))
                    new_rels.append(
                        RelationshipAssertion(extra_info="Inferred", person=sib.related_person,
                                              related_person=father.related_person,
                                              relationship=father.get_inverse_relationship()))
            # Verify children
            if spouse != None:
                for kid in children:
                    if spouse.related_person.sex.name == "Male" and RelationshipAssertion.objects.filter(
                            related_person=sib.related_person,
                            relationship__name="father of").count() == 0:
                        new_rels.append(
                            RelationshipAssertion(extra_info="Inferred", related_person=spouse.related_person,
                                                  person=kid.related_person,
                                                  relationship=type_son))
                        new_rels.append(
                            RelationshipAssertion(extra_info="Inferred", person=spouse.related_person,
                                                  related_person=kid.related_person,
                                                  relationship=type_father))

                    if spouse.related_person.sex.name == "Female" and RelationshipAssertion.objects.filter(
                            related_person=sib.related_person,
                            relationship__name="mother of").count() == 0:
                        new_rels.append(
                            RelationshipAssertion(extra_info="Inferred", related_person=spouse.related_person,
                                                  person=kid.related_person,
                                                  relationship=type_daughter))
                        new_rels.append(
                            RelationshipAssertion(extra_info="Inferred", person=spouse.related_person,
                                                  related_person=kid.related_person,
                                                  relationship=type_mother))
            return new_rels

        # Check they are also have parents listed
        # Add if not


        # Siblings
        return new_rels

    # When none left exit

    def add_inverse_relationships(self):
        new_invs = []
        for relassert in RelationshipAssertion.objects.all():
            # Get inverse of relationship
            inv_type = relassert.get_inverse_relationship()
            if inv_type is not None:
                # Check if inverse already exists
                invs = RelationshipAssertion.objects.filter(person=relassert.related_person,
                                                            related_person=relassert.person, relationship=inv_type)
                if invs.count() == 0:
                    # Add inverse relationship
                    inv = RelationshipAssertion(extra_info="Inferred", person=relassert.related_person,
                                                related_person=relassert.person,
                                                relationship=inv_type)
                    # inv.save()
                    new_invs.append(inv)
                else:
                    inv = invs[0]
                    # todo Link to original
        return new_invs

    def handle(self, *args, **options):  # noqa

        now = datetime.datetime.now()
        date = now.strftime("%d_%B_%Y")
        log_fname = "inverse_relationship-log_{}.csv".format(date)

        with open(log_fname, 'wb') as ofile:
            csv_log = csv.DictWriter(
                ofile,
                [
                    "person",
                    "related_person",
                    "inverse_relationship_type",
                    "id",
                    "inferred_person",
                    "inferred_related_person",
                    "inferred_relationship_type",

                ],
                dialect='excel',
                delimiter=",",
                extrasaction='ignore')
            csv_log.writeheader()
            new_invs = self.add_inverse_relationships()
            # todo When saving Iterate this until no new relationships created
            new_rels=self.add_inferred_relationships()

        print("Wrote {}".format(log_fname))
