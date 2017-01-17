

from django.core.management.base import BaseCommand
import logging
from promrep.models import Person, Office
from django.db.models import Q
import csv
import datetime


class Command(BaseCommand):
    args = '<page document_path document_path ...>'
    help = 'Adds the Highest office info to the Person model'

    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):  # noqa

        now = datetime.datetime.now()
        date = now.strftime("%d_%B_%Y")
        log_fname = "highest_office-log_{}.csv".format(date)

        with open(log_fname, 'wb') as ofile:
            csv_log = csv.DictWriter(
                ofile,
                [
                    "id",
                    "name",
                    "highest_office",
                ],
                dialect='excel',
                delimiter=",",
                extrasaction='ignore')
            csv_log.writeheader()




                # csv_log.writerow({
                #                  "id": p.id,
                #                  "name": p,
                #                  "highest_office": hoffice
                #                  })

        print("Wrote {}".format(log_fname))

