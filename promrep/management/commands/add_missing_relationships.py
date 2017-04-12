import csv
import datetime
import logging

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management.base import BaseCommand
from django.db.models import Q

from promrep.models import Person, RelationshipAssertion, RelationshipType
from promrep.models import SecondarySource, RelationshipInverse


# Populate inferred family relationships based on rules in DPRR-257
# IMPORTANT NOTE: Assumes inverse relationships already populated
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
                inverse = RelationshipInverse.objects.get(
                    relationship=relationship,
                    sex=person.sex)
                new_assert = RelationshipAssertion(
                    extra_info="Inferred",
                    person=person,
                    related_person=found.person,
                    secondary_source=dprr_source,
                    relationship=inverse.inverse_relationship)
                relationships.append(new_assert)
                self.writeassetion(new_assert, found)
                if single:
                    break
        return relationships

    def reset_assertions(self):
        RelationshipAssertion.objects.filter(
            extra_info="Inferred", is_verified=False).delete()
        RelationshipAssertion.objects.filter(
            extra_info="Inferred Inverse", is_verified=False).delete()
        RelationshipAssertion.objects.filter(
            extra_info="Inferred Inverse 1", is_verified=False).delete()
        RelationshipAssertion.objects.filter(
            extra_info="Inferred Inverse 2", is_verified=False).delete()
        RelationshipAssertion.objects.filter(
            extra_info="Inferred Inverse 3", is_verified=False).delete()

    def writeassetion(self, new_assert, source_assert):
        print new_assert
        dprr_source = SecondarySource.objects.get(name='DPRR Team')
        # Final check to weed out duplicates
        if (RelationshipAssertion.objects.filter(
                person=new_assert.person,
                related_person=new_assert.related_person,
                relationship=new_assert.relationship).count() == 0):
            new_assert.uncertain = True
            new_assert.save()
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
            inv_type = RelationshipInverse.objects.get(
                relationship=new_assert.relationship,
                sex=new_assert.related_person.sex)
            if RelationshipAssertion.objects.filter(
                    person=new_assert.related_person,
                    related_person=new_assert.person,
                    relationship=inv_type.inverse_relationship).count() == 0:
                new_inv = RelationshipAssertion(
                    extra_info="Inferred Inverse",
                    person=new_assert.related_person,
                    related_person=new_assert.person,
                    uncertain=True,
                    secondary_source=dprr_source,
                    relationship=inv_type.inverse_relationship)
                new_inv.save()

    def add_inferred_relationships(self):
        new_rels = []
        type_mother = RelationshipType.objects.get(name="mother of")
        type_father = RelationshipType.objects.get(name="father of")
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
                # check the siblings' siblings
                related_siblings = RelationshipAssertion.objects.filter(
                    Q(person=sib.related_person),
                    Q(relationship__name="brother of") |
                    Q(relationship__name="sister of"))
                for related_sibling in related_siblings:
                    if related_sibling.related_person != person:
                        if related_sibling.related_person.sex.name == "Male":
                            sib_relationship = RelationshipType.objects.get(
                                name="brother of")
                        else:
                            sib_relationship = RelationshipType.objects.get(
                                name="sister of")
                        new_sibling = RelationshipAssertion(
                            extra_info="Inferred",
                            secondary_source=dprr_source,
                            person=related_sibling.related_person,
                            related_person=person,
                            relationship=sib_relationship)
                        self.writeassetion(new_sibling, related_sibling)

            # Verify children
            if spouse is not None:
                for kid in children:
                    if (spouse.related_person.sex.name == "Male" and
                        RelationshipAssertion.objects.filter(
                            related_person=kid.related_person,
                            relationship__name="father of").count() == 0):
                        new_type = RelationshipInverse.objects.get(
                            relationship__name="father of",
                            sex=kid.related_person.sex)
                        new_assert = RelationshipAssertion(
                            extra_info="Inferred Inverse",
                            related_person=spouse.related_person,
                            person=kid.related_person,
                            secondary_source=dprr_source,
                            relationship=new_type.inverse_relationship)
                        new_rels.append(new_assert)
                        self.writeassetion(new_assert, spouse)

                    if (spouse.related_person.sex.name == "Female" and
                        RelationshipAssertion.objects.filter(
                            related_person=kid.related_person,
                            relationship__name="mother of").count() == 0):
                        new_type = RelationshipInverse.objects.get(
                            relationship__name="mother of",
                            sex=kid.related_person.sex)
                        new_assert = RelationshipAssertion(
                            extra_info="Inferred",
                            related_person=spouse.related_person,
                            secondary_source=dprr_source,
                            person=kid.related_person,
                            relationship=new_type.inverse_relationship)
                        new_rels.append(new_assert)
                        self.writeassetion(new_assert, spouse)

            # Make sure children are listed as siblings of one another
            for kid in children:
                if kid.related_person.sex.name == "Male":
                    sib_relationship = RelationshipType.objects.get(
                        name="brother of")
                else:
                    sib_relationship = RelationshipType.objects.get(
                        name="sister of")
                for sib in children:
                    if sib != kid and RelationshipAssertion.objects.filter(
                            Q(person=kid.related_person),
                            Q(related_person=sib.related_person),
                            Q(relationship__name="brother of") |
                            Q(relationship__name="sister of")
                    ).count() == 0:
                        new_sib = RelationshipAssertion(
                            person=kid.related_person,
                            related_person=sib.related_person,
                            relationship=sib_relationship,
                            extra_info="Inferred",
                            secondary_source=dprr_source,
                        )
                        self.writeassetion(new_sib, sib)
        return new_rels

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
            self.reset_assertions()
            self.add_inferred_relationships()
        print("Wrote {}".format(log_fname))
