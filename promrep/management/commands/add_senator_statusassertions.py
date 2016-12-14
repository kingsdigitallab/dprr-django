# -*- coding: utf-8 -*-

# this script enriches the database with the Senator StatusAssertions
#   for full rules and dicussion please see the original JIRA ticket here:
#   https://jira.dighum.kcl.ac.uk/projects/DPRR/issues/DPRR-256


from django.db.models import Q

from promrep.models import (
    Office, Person, SecondarySource, StatusAssertion, StatusType
)
import datetime
import csv


def run():
    # This process affects each person who has a post assertion with a start
    # date after -180, for the following offices - quaestor, tribunis plebis,
    # aedilis (and subtypes), praetor (and subtypes), consul (and subtypes),
    # censor (and subtypes), princeps senatus and senator including the
    # different subtypes - senator quaestorius, praetorius consularis etc)

    # If a person has post assertion as listed above except senator and its
    # subtypes, then create a senator status assertion

    now = datetime.datetime.now()
    date = now.strftime("%d_%B_%Y")
    log_fname = "senator_data_log-{}.csv".format(date)

    status_type, created = StatusType.objects.get_or_create(name="senator")
    sec_source, created = SecondarySource.objects.get_or_create(
        name="DPRR Team")

    non_senator_offices_list = ['quaestor', 'tribunus plebis', 'aedilis',
                                'praetor', 'consul', 'censor',
                                'princeps senatus', ]

    # these should not be considered
    off_exclusions = ['tr. pl. des.', 'q. desig.']
    off_exc_list = [
        Office.objects.get(abbrev_name=o) for o in off_exclusions
    ]

    # all offices EXCEPT senator and subtypes
    non_sen_offices = []

    for oname in non_senator_offices_list:
        off = Office.objects.get(name=oname)
        non_sen_offices += list(off.get_descendants(include_self=True))

    non_senator_offices = [o for o in non_sen_offices if o not in off_exc_list]

    non_sen_q = Q(post_assertions__office__in=non_senator_offices)

    senator_offices = Office.objects.get(
        name='senator').get_descendants(include_self=True)
    sen_q = Q(post_assertions__office__in=senator_offices)

    only_senators = Person.objects.filter(sen_q).exclude(non_sen_q).distinct()

    # sen_and_other = Person.objects.filter(sen_q).filter(non_sen_q).distinct()
    # oth_senatorial = \
    # Person.objects.exclude(sen_q).filter(non_sen_q).distinct()
    all_senatorial = Person.objects.filter(sen_q | non_sen_q).filter(
        post_assertions__date_start__gte=-180).distinct()

    print("Will add {} new Senator SAssertions".format(all_senatorial.count()))

    with open(log_fname, 'wb') as ofile:
        csv_log = csv.DictWriter(
            ofile,
            [
                "person",
                "statusassertion",
                "date_start",
                "date_start_uncertain",
                "date_end",
                "date_end_uncertain",
                "first_qualifying_office",
                "first_qualifying_date",
                "last_office_date",
                "last_life_date",
                "last_life_date_uncertain",
                "last_life_date_type"
            ],
            dialect='excel',
            delimiter=",",
            extrasaction='ignore')
        csv_log.writeheader()

        # If a person is listed with a senator post assertion but none of
        #   the other senatorial offices -> create a senator status assertion
        #   with the same start/end dates as the existing senator PostAssertion

        # for person in Person.objects.filter(id__in=[1565]):
        for person in all_senatorial:
            sa = StatusAssertion(
                person=person,
                status=status_type,
                secondary_source=sec_source,
            )

            log_dict = {
                'person': person.id,
            }

            last_life_date = get_last_life_date(person)
            log_dict.update(last_life_date)

            if person in only_senators:
                sen_postassertions = person.post_assertions.filter(
                    office__in=senator_offices).order_by('date_start')

                sa.date_start = sen_postassertions.first().date_start

                # TODO: should use date start instead?
                sa.date_end = sen_postassertions.last().date_end
                sa.date_end_uncertain = sen_postassertions.last()\
                    .date_end_uncertain
                sa.save()

                log_dict.update({
                    'first_qualifying_office': 'senator',
                    'first_qualifying_date': sa.date_start,
                    'last_office_date': sa.date_end,
                })

            else:
                pa_list = person.post_assertions.filter(
                    Q(office__in=non_senator_offices) |
                    Q(office__in=senator_offices)).order_by('date_start')

                date_start_dict = get_date_start(pa_list)

                log_dict['first_qualifying_office'] = \
                    date_start_dict['first_qualifying_office']

                sa.date_start = date_start_dict['date_start']
                sa.date_start_uncertain = date_start_dict[
                    'date_start_uncertain']

                # to compute the end date we want *any* office
                last_pa = person.post_assertions.order_by('date_start').last()
                date_last_office = last_pa.date_end

                use_last_life_date = False

                if last_life_date:
                    if last_life_date['last_life_date'] > date_last_office:
                        use_last_life_date = True

                if use_last_life_date:
                    sa.date_end = last_life_date['last_life_date']
                    sa.date_end_uncertain = last_life_date[
                        'last_life_date_uncertain']
                    sa.save()
                else:
                    sa.date_end = date_last_office
                    sa.date_end_uncertain = True
                    sa.save()

                log_dict.update({
                    'first_qualifying_date': date_start_dict['date_start'],
                    'last_qualifying_office': last_pa.office.name,
                    'last_office_date': sa.date_end,
                })

            log_dict.update(
                {
                    'statusassertion': sa.id,
                    'date_start': sa.date_start,
                    'date_start_uncertain': sa.date_start_uncertain,
                    'date_end': sa.date_end,
                    'date_end_uncertain': sa.date_end_uncertain,
                })

            csv_log.writerow(log_dict)

    print("Wrote {}".format(log_fname))


def get_date_start(post_assertions):
    """Given a list of postassertions, returns a dictionary
     with the start date, uncertainty and debug data
    """
    date_start = None
    uncertain = False
    office_name_log = ""

    aed_list = [o.name for o in Office.objects.get(
        name="aedilis").get_descendants(include_self=True)]

    pra_list = [o.name for o in Office.objects.get(
        name="praetor").get_descendants(include_self=True)]

    con_list = [o.name for o in Office.objects.get(
        name="consul").get_descendants(include_self=True)]

    tri_list = [o.name for o in Office.objects.get(
        name="tribunus plebis").get_descendants(include_self=True)]

    sen_list = [o.name for o in Office.objects.get(
        name="senator").get_descendants(include_self=True)]

    qua_list = [o.name for o in Office.objects.get(
        name="quaestor").get_descendants(include_self=True)]

    pri_list = [o.name for o in Office.objects.get(
        name="princeps senatus").get_descendants(include_self=True)]

    cen_list = [o.name for o in Office.objects.get(
        name="censor").get_descendants(include_self=True)]

    offices_list = aed_list + pra_list + con_list + tri_list + \
        sen_list + qua_list + cen_list + pri_list

    # If person has a quaestor post assertion, then set the start date of the
    # senator post assertion = quaestor start date + 1
    # same certainty as postasserion

    # TODO: add princeps senatus and censores
    pa_list = post_assertions.filter(
        office__name__in=offices_list,
        date_start__gte=-180).order_by('date_start')

    if pa_list.exists():

        earliest_pa = pa_list.first()
        office_name = earliest_pa.office.name
        # if the person has no quaestor post assertion
        office_name_log = "{} ({})".format(
            office_name,
            earliest_pa.date_start
        )

        if office_name in sen_list:
            date_start = earliest_pa.date_start
            uncertain = earliest_pa.date_start_uncertain
            office_name_log = "{} ({})".format(
                earliest_pa.office.name, earliest_pa.date_start)

        elif office_name in qua_list:
            date_start = earliest_pa.date_start + 1
            uncertain = earliest_pa.date_start_uncertain
            office_name_log = "{} ({})".format(
                earliest_pa.office.name, earliest_pa.date_start)

        elif office_name in aed_list:
            # earliest postassertion is aedile (and subtypes)
            # start date of the senator post assertion is the start date of
            # the aedileship - 2, certainty = uncertain

            date_start = earliest_pa.date_start - 2
            uncertain = True

        elif office_name in tri_list:
            # earliest post assertion is tribune of the plebs and subtypes
            # start date of the senator status assertion to the start
            # date of the tribunate of the plebs,
            # certainty = the same as the post assertion

            date_start = earliest_pa.date_start
            uncertain = earliest_pa.date_start_uncertain

        elif office_name in pra_list:
            # earliest postassertion is praetor (and subtypes)
            # start date of the senator post assertion is the start date of
            # the praetorship - 2, certainty = uncertain

            date_start = earliest_pa.date_start - 2
            uncertain = True
        elif office_name in con_list:
            # earliest post assertion is consul (and subtypes)
            # start date of the senator post assertion to the start date of
            # the consulship - 5, certainty = uncertain

            date_start = earliest_pa.date_start - 5
            uncertain = True
        else:
            date_start = earliest_pa.date_start - 5
            uncertain = earliest_pa.date_start_uncertain

            # print("Couldn't start date: person {}, office {}".format(
            #     earliest_pa.person.id, office_name_log))

    odict = {
        'date_start': date_start,
        'date_start_uncertain': uncertain,
        'first_qualifying_office': office_name_log
    }

    return odict


def get_last_life_date(person):
    """For a given person returns a dictionary
    with the last senate related life date
    as well as type and certainty
    """

    #   The only time we can be sure that a person is no longer a senator
    #   is when they are dead (all types !!), exiled or expelled.)

    date_dict = {}

    date_types = ["death", "death - natural", "death - violent",
                  "exile", "expelled from Senate", "extradited",
                  "proscribed"]

    dates = person.dateinformation_set.filter(
        date_type__name__in=date_types).order_by('value')

    if dates.exists():
        # If the person has a life date of expelled or exiled or death or
        #   death - violent, set the end date of the senator status assertion
        #   to the earliest of these life dates, certainty = the same
        #   certainty as the life date

        date_dict['last_life_date'] = dates.first().value
        date_dict['last_life_date_uncertain'] = dates.first().uncertain
        date_dict['last_life_date_type'] = dates.first().date_type.name

    return date_dict
