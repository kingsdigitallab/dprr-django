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

        cos_Q = Q(office__name__in=cos_list)
        pra_Q = Q(office__name__in=pra_list)
        aed_Q = Q(office__name__in=aed_list)
        tri_Q = Q(office__name__in=tri_list)
        qua_Q = Q(office__name__in=qua_list)

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

            # don't overwrite manually edited fields
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
                pas = p.post_assertions.filter(
                    cos_Q | pra_Q | aed_Q | tri_Q | qua_Q).order_by(
                    'date_start')

                sas = p.statusassertion_set.all().order_by('date_start')

                if pas.exists():
                    off = ""
                    date = ""

                    cos = pas.filter(cos_Q)
                    pra = pas.filter(pra_Q)
                    aed = pas.filter(aed_Q)
                    tri = pas.filter(tri_Q)
                    qua = pas.filter(qua_Q)

                    # TODO: test if any of these exist!!!
                    if cos.exists():
                        off = cos.first().office_str()
                        date = cos.first().print_date()
                    elif pra.exists():
                        off = pra.first().office_str()
                        date = pra.first().print_date()
                    elif aed.exists():
                        off = aed.first().office_str()
                        date = aed.first().print_date()
                    elif tri.exists():
                        off = tri.first().office_str()
                        date = tri.first().print_date()
                    elif qua.exists():
                        off = qua.first().office_str()
                        date = qua.first().print_date()

                    if not date:
                        date = "uncertain date"

                    if off and date:
                        hoffice = "{} {}".format(off, date)

                elif sas.exists():
                    off = sas.first().status.get_display_name()
                    date = sas.first().date_start

                    # See DPRR-385
                    if off == "eq. R.":
                        if not date:
                            date = "?"
                        else:
                            date = ""
                    elif date is not None:
                        date = abs(date)
                    else:
                        date = "uncertain date"

                    if off and date:
                        if date == "?":
                            hoffice = "{}?".format(off)
                        else:
                            hoffice = "{} {}".format(off, date)
                    elif off:
                        hoffice = "{}".format(off)

                # TODO: we're only checking direct, because we expect to calc
                #     the inverse relationships - see DPRR-257
                # - some inverse relationships checked.
                # Highest relationship
                elif p.relationships_as_subject.exists() or\
                        p.relationships_as_object.exists():

                    rel_per = None
                    rel_str = ""
                    rel_unc = False

                    son_q = Q(relationship__name="son of")
                    dau_q = Q(relationship__name="daughter of")
                    wife_q = Q(relationship__name="married to")
                    father_q = Q(relationship__name="father of")

                    rel_is_male_q = Q(related_person__sex__name="Male")
                    pers_is_male_q = Q(person__sex__name="Male")

                    # son of male
                    ra_son = p.relationships_as_subject.filter(
                        son_q, rel_is_male_q)

                    # daughter of male
                    ra_dau = p.relationships_as_subject.filter(
                        dau_q, rel_is_male_q)

                    # Inverse "father of":
                    ra_father = p.relationships_as_object.filter(
                        father_q, pers_is_male_q)

                    # wife of male
                    ra_wife = p.relationships_as_subject.filter(
                        wife_q, pers_is_male_q)

                    # inverse wife of male
                    ra_wife_inv = p.relationships_as_object.filter(
                        wife_q, rel_is_male_q)

                    ra_any = p.relationships_as_subject.all()

                    # son of (male) display as (s.), otherwise
                    if ra_son.exists():
                        rel_str = ra_son.first().relationship.name
                        rel_per = ra_son.first().related_person
                        rel_unc = ra_son.first().uncertain

                    # son/daughter of (male) display as (s.), otherwise
                    elif ra_father.exists():
                        if p.sex.name == "Male":
                            rel_str = "son of"
                        else:
                            rel_str = "daughter of"
                        rel_per = ra_father.first().person
                        rel_unc = ra_father.first().uncertain

                    # daughter of (male) display as (d.), otherwise
                    elif ra_dau.exists():
                        rel_str = ra_dau.first().relationship.name
                        rel_per = ra_dau.first().related_person
                        rel_unc = ra_dau.first().uncertain

                    # wife of (male) display as (w.), otherwise
                    elif ra_wife.exists():
                        rel_str = ra_wife.first().relationship.name
                        rel_per = ra_wife.first().related_person
                        rel_unc = ra_wife.first().uncertain

                    # wife of (male) display as (w.), otherwise
                    elif ra_wife_inv.exists():
                        rel_str = ra_wife_inv.first().relationship.name
                        rel_per = ra_wife_inv.first().person
                        rel_unc = ra_wife_inv.first().uncertain

                    # any other relationship else
                    elif ra_any.exists():
                        rel_str = ra_any.first().relationship.name
                        rel_unc = ra_any.first().uncertain
                        rel_per = ra_any.first().related_person

                    if rel_unc:
                        unc_str = "?"
                    else:
                        unc_str = ""

                    if rel_per and rel_str:
                        # Get the related person's highest office:
                        rel_per_ho = rel_per.get_real_highest_office()
                        if rel_per_ho:
                            hoffice = "{}{} {} ({})".format(rel_str, unc_str,
                                                            rel_per,
                                                            rel_per_ho)
                        else:
                            hoffice = "{}{} {}".format(rel_str, unc_str,
                                                       rel_per)

                # default case, print the last office the person had
                if hoffice == "":
                    if p.post_assertions.exists():
                        pa = p.post_assertions.order_by('-date_start').first()
                        off = pa.office_str()

                        date = pa.print_date()

                        if off and date:
                            hoffice = "{} {}".format(off, date)

                p.highest_office = hoffice
                p.save()

                csv_log.writerow({
                                 "id": p.id,
                                 "name": p,
                                 "highest_office": hoffice
                                 })

        print("Wrote {}".format(log_fname))
