from django.core.management.base import BaseCommand
import logging
from promrep.models import Person, RelationshipAssertion, RelationshipType
from django.db.models import Q
import csv
import datetime


class Command(BaseCommand):
    args = '<page document_path document_path ...>'
    help = 'Adds inverse relationships if they do no exist'

    logger = logging.getLogger(__name__)

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
                    "original_person",
                    "original_related_person",
                    "original_relationship_type",

                ],
                dialect='excel',
                delimiter=",",
                extrasaction='ignore')
            csv_log.writeheader()
            for relassert in RelationshipAssertion.objects.all():
                # Get inverse of relationship
                inv_type = relassert.get_inverse_relationship()
                if inv_type is not None:
                    # Check if inverse already exists
                    invs = RelationshipAssertion.objects.filter(person=relassert.related_person,
                                                                related_person=relassert.person, relationship=inv_type)
                    if invs.count() == 0:
                        # Add inverse relationship
                        inv = RelationshipAssertion(person=relassert.related_person, related_person=relassert.person,
                                                    relationship=inv_type)
                        # inv.save()
                        csv_log.writerow({
                            "person": inv.person,
                            "related_person": inv.related_person,
                            "inverse_relationship_type": inv.relationship,
                            "id": relassert.id,
                            "original_person": relassert.person,
                            "original_related_person": relassert.related_person,
                            "original_relationship_type": relassert.relationship,
                        })
                    else:
                        inv = invs[0]
                        # todo Link to original

        print("Wrote {}".format(log_fname))
