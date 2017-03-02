from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import logging
from promrep.models import Person, RelationshipAssertion, RelationshipType
from promrep.models import SecondarySource
import csv
import datetime


# EHall 19/1/2017

class Command(BaseCommand):
    args = '<page document_path document_path ...>'
    help = 'Adds inverse relationships if they do no exist'

    logger = logging.getLogger(__name__)
    csv_log = None

    def findfromsiblings(self, person, sibs, relationship, single):
        relationships = []
        dprr_source = SecondarySource.objects.get(name='DPRR Team')
        for sib in sibs:
            try:
                found = RelationshipAssertion.objects.get(
                    related_person=sib.related_person,
                    secondary_source=dprr_source,
                    relationship=relationship)
            except ObjectDoesNotExist:
                found = None
            except MultipleObjectsReturned:
                found = None
            if found is not None:
                new_assert = RelationshipAssertion(
                    extra_info="Inferred",
                    person=person,
                    related_person=found.person,
                    secondary_source=dprr_source,
                    relationship=relationship)
                relationships.append(new_assert)
                self.writeassetion(new_assert, found)
                if single:
                    break
        return relationships

    def writeassetion(self, new_assert, source_assert):
        print new_assert
        # new_assert.save()
        self.csv_log.writerow({
            "inferred_person_id": new_assert.person.id,
            "inferred_person": new_assert.person,
            "inferred_related_person_id": new_assert.related_person.id,
            "inferred_related_person": new_assert.related_person,
            "inferred_relationship_type": new_assert.relationship,
            "uncertain": new_assert.uncertain,
            "secondary source": new_assert.secondary_source,
            "assertion_id": source_assert.id,
            "source_person_id": source_assert.person.id,
            "source_person": source_assert.person,
            "source_related_person_id": source_assert.related_person.id,
            "source_related_person": source_assert.related_person,
            "source_relationship_type": source_assert.relationship,
        })

    # Populate inferred family relationships based on rules in DPRR-257
    # IMPORTANT NOTE: Assumes inverse relationships already populated
    def add_inferred_relationships(self):
        new_rels = []
        type_mother = RelationshipType.objects.get(name="mother of")
        type_father = RelationshipType.objects.get(name="father of")
        type_son = RelationshipType.objects.get(name="son of")
        type_daughter = RelationshipType.objects.get(name="daughter of")
        dprr_source = SecondarySource.objects.get(name='DPRR Team')
        for person in Person.objects.all():
            sibs = []
            children = []
            mother = None
            father = None
            spouse = None
            # Sort relationships into family members
            for relassert in RelationshipAssertion.objects.filter(
                    person=person).distinct():
                # Mother/Father
                if (relassert.relationship.name == "father of" or
                        relassert.relationship.name == "mother of"):
                    children.append(relassert)
                elif (relassert.relationship.name == "son of" or
                        relassert.relationship.name == "daughter of"):
                    # Son/Daughter
                    if relassert.related_person.sex.name == "Male":
                        father = relassert
                    else:
                        mother = relassert
                elif (relassert.relationship.name == "brother of" or
                        relassert.relationship.name == "sister of"):
                    sibs.append(relassert)
                elif relassert.relationship.name == "married to":
                    spouse = relassert
            # Check for father and mother
            if father is None and len(sibs) > 0:
                finds = self.findfromsiblings(person, sibs, type_father, True)
                if len(finds) > 0:
                    # TODO save father
                    father = finds[0]
                    new_rels.append(father)
            if mother is None and len(sibs) > 0:
                finds = self.findfromsiblings(person, sibs, type_mother, True)
                if len(finds) > 0:
                    # TODO save
                    mother = finds[0]
                    new_rels.append(mother)

            # Go through siblings and make sure their parent records are
            # complete
            for sib in sibs:
                if mother is not None and \
                    RelationshipAssertion.objects.filter(
                        related_person=sib.related_person,
                        relationship=type_mother).count() == 0:
                    new_assert = RelationshipAssertion(
                        extra_info="Inferred",
                        related_person=sib.related_person,
                        person=mother.related_person,
                        secondary_source=dprr_source,
                        relationship=type_mother)
                    new_rels.append(new_assert)
                    self.writeassetion(new_assert, sib)
                    new_inv = RelationshipAssertion(
                        extra_info="Inferred", person=sib.related_person,
                        related_person=mother.related_person,
                        relationship=mother.relationship)
                    new_rels.append(new_inv)
                    # self.writeassetion(new_inv, sib)
                if father is not None \
                        and RelationshipAssertion.objects.filter(
                            related_person=sib.related_person,
                            relationship=type_father).count() == 0:
                    new_assert = RelationshipAssertion(
                        extra_info="Inferred",
                        related_person=sib.related_person,
                        person=father.related_person,
                        secondary_source=dprr_source,
                        relationship=type_father)
                    new_rels.append(new_assert)
                    self.writeassetion(new_assert, sib)
                    new_rels.append(
                        RelationshipAssertion(
                            extra_info="Inferred", person=sib.related_person,
                            related_person=father.related_person,
                            relationship=father.relationship))
            # Verify children
            if spouse is not None:
                for kid in children:
                    if (spouse.related_person.sex.name == "Male" and
                            RelationshipAssertion.objects.filter(
                            related_person=sib.related_person,
                            relationship__name="father of").count() == 0):
                        new_assert = RelationshipAssertion(
                            extra_info="Inferred",
                            related_person=spouse.related_person,
                            person=kid.related_person,
                            secondary_source=dprr_source,
                            relationship=type_son)
                        new_rels.append(new_assert)
                        self.writeassetion(new_assert, spouse)
                        new_inv = RelationshipAssertion(
                            extra_info="Inferred",
                            person=spouse.related_person,
                            related_person=kid.related_person,
                            secondary_source=dprr_source,
                            relationship=type_father)
                        new_rels.append(new_inv)
                        # self.writeassetion(new_inv, spouse)

                    if (spouse.related_person.sex.name == "Female" and
                            RelationshipAssertion.objects.filter(
                            related_person=sib.related_person,
                            relationship__name="mother of").count() == 0):
                        new_assert = RelationshipAssertion(
                            extra_info="Inferred",
                            related_person=spouse.related_person,
                            secondary_source=dprr_source,
                            person=kid.related_person,
                            relationship=type_daughter)
                        new_rels.append(new_assert)
                        self.writeassetion(new_assert, spouse)
                        new_inv = RelationshipAssertion(
                            extra_info="Inferred",
                            person=spouse.related_person,
                            secondary_source=dprr_source,
                            related_person=kid.related_person,
                            relationship=type_mother)
                        new_rels.append(new_inv)
                        # self.writeassetion(new_inv, spouse)

        return new_rels

    def add_inverse_relationships(self):
        new_invs = []
        for relassert in RelationshipAssertion.objects.all():
            # Get inverse of relationship
            inv_type = relassert.get_inverse_relationship()
            if inv_type is not None:
                # Check if inverse already exists
                invs = RelationshipAssertion.objects.filter(
                    person=relassert.related_person,
                    related_person=relassert.person, relationship=inv_type)
                if invs.count() == 0:
                    # Add inverse relationship
                    inv = RelationshipAssertion(
                        extra_info="Inferred", person=relassert.related_person,
                        related_person=relassert.person,
                        relationship=inv_type)
                    # inv.save()
                    new_invs.append(inv)
                else:
                    inv = invs[0]
                # todo Link to original
                relassert.inverse_relationship = inv
        return new_invs

    def handle(self, *args, **options):  # noqa

        now = datetime.datetime.now()
        date = now.strftime("%d_%B_%Y")
        log_fname = "inferred_relationship-log_{}.csv".format(date)

        with open(log_fname, 'wb') as ofile:
            csv_log = csv.DictWriter(
                ofile,
                [
                    "inferred_person_id",
                    "inferred_person",
                    "inferred_relationship_type",
                    "uncertain",
                    "secondary source",
                    "inferred_related_person_id",
                    "inferred_related_person",
                    "assertion_id",
                    "source_person_id",
                    "source_person",
                    "source_relationship_type",
                    "source_related_person",
                ],
                dialect='excel',
                delimiter=",",
                extrasaction='ignore')
            self.csv_log = csv_log
            csv_log.writeheader()
            # todo run inverse first when saving
            # self.add_inverse_relationships()
            # todo When saving Iterate this until no new relationships created
            self.add_inferred_relationships()
        print("Wrote {}".format(log_fname))
