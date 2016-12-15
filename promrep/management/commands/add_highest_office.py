from django.core.management.base import BaseCommand
import logging
from promrep.models import Person, Office
from django.db.models import Q
import csv
import datetime


class Command(BaseCommand):
    args = '<page document_path document_path ...>'
    help = 'Adds the Highest office info to the Persons'

    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):  # noqa

        now = datetime.datetime.now()
        date = now.strftime("%d_%B_%Y")
        log_fname = "highest_office-log_{}.csv".format(date)

        cos_list = [o.name for o in Office.objects.get(
            name="consul").get_descendants(include_self=True)]

        pra_list = [o.name for o in Office.objects.get(
            name="praetor").get_descendants(include_self=True)]

        aed_list = [o.name for o in Office.objects.get(
            name="aedilis").get_descendants(include_self=True)]

        tri_list = [o.name for o in Office.objects.get(
            name="tribunus plebis").get_descendants(include_self=True)]

        qua_list = [o.name for o in Office.objects.get(
            name="quaestor").get_descendants(include_self=True)]

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

            persons = Person.objects.filter(highest_office_edited=False)
            print("Adding highest office info: {} persons".format(
                persons.count()))

            for p in persons:
                hoffice = ""

                # cos. if achieved (first one), otherwise
                # pr. if achieved,(first one), otherwise
                # aed. if achieved,(first, either aed., pl. or cur.), otherwise
                # tr.pl. if achieved,(first one), otherwise
                # q. if achieved,(first one), otherwise
                # sen. if achieved/eq. R.
                pas = p.post_assertions.order_by('date_start')

                if pas.exists():
                    off = ""
                    date = ""

                    cos = pas.filter(office__name__in=cos_list)
                    pra = pas.filter(office__name__in=pra_list)
                    aed = pas.filter(office__name__in=aed_list)
                    tri = pas.filter(office__name__in=tri_list)
                    qua = pas.filter(office__name__in=qua_list)
                    sas = p.statusassertion_set.all().order_by('date_start')

                    # TODO: test if any of these exist!!!
                    if cos.exists():
                        off = cos.first().office.abbrev_name
                        date = cos.first().date_start
                    elif pra.exists():
                        off = pra.first().office.abbrev_name
                        date = pra.first().date_start
                    elif aed.exists():
                        off = aed.first().office.abbrev_name
                        date = aed.first().date_start
                    elif tri.exists():
                        off = tri.first().office.abbrev_name
                        date = tri.first().date_start
                    elif qua.exists():
                        off = qua.first().office.abbrev_name
                        date = qua.first().date_start
                    elif sas.exists():
                        off = sas.first().status.name
                        date = sas.first().date_start

                    if off and date:
                        try:
                            date = -int(date)
                        except:
                            pass
                        hoffice = "{} ({} B.C.)".format(off, date)

                # TODO: we're only checking direct, because we expect to calc
                #     the inverse relationships - see DPRR-257
                # Highest relationship
                elif p.relationships_as_object.exists():

                    rel_per = None
                    rel_str = ""

                    son_q = Q(relationship__name="son of")
                    dau_q = Q(relationship__name="daughter of")
                    wif_q = Q(relationship__name="wife of")

                    rel_is_male_q = Q(related_person__sex__name="Male")

                    ra_son = p.relationships_as_object.filter(
                        son_q and rel_is_male_q)
                    ra_dau = p.relationships_as_object.filter(
                        dau_q and rel_is_male_q)
                    ra_wif = p.relationships_as_object.filter(wif_q)

                    ra_any = p.relationships_as_object.all()

                    # son of (male) display as (s.), otherwise
                    if ra_son.exists():
                        rel_str = "s. of"
                        rel_per = ra_son.first().related_person
                    # daughter of (male) display as (d.), otherwise
                    elif ra_dau.exists():
                        rel_str = "d. of"
                        rel_per = ra_dau.first().related_person
                    # wife of display as (w.), otherwise
                    elif ra_wif.exists():
                        rel_str = "w. of"
                        rel_per = ra_dau.first().related_person
                    # any other relationship else
                    elif ra_any.exists():
                        rel_str = ra_any.first().relationship
                        rel_per = ra_any.first().related_person

                    if rel_per and rel_str:
                        hoffice = "{} {}".format(rel_str, rel_per)

                csv_log.writerow({
                                 "id": p.id,
                                 "name": p,
                                 "highest_office": hoffice
                                 })

        print("Wrote {}".format(log_fname))
