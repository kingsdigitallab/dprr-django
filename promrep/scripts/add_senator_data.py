# -*- coding: utf-8 -*-

# this script enriches the database with the Senator StatusAssertions
#   for full rules and dicussion please see the original JIRA ticket here:
#   https://jira.dighum.kcl.ac.uk/projects/DPRR/issues/DPRR-256


from promrep.models import (
    Office, Person, PostAssertion, SecondarySource, StatusAssertion,
    StatusType
)
import datetime
import csv


def run():
    print("Adding Senator Status Assertions")

    status_type, created = StatusType.objects.get_or_create(name="senator")
    sec_source, created = SecondarySource.objects.get_or_create(
        name="DPRR Team")

    non_senator_offices_list = ['quaestor', 'tribunus plebis', 'aedilis',
                                'praetor', 'consul', 'censor',
                                'princeps senatus', ]

    # all offices EXCEPT senator and subtypes
    non_senator_offices = []

    for oname in non_senator_offices_list:
        off = Office.objects.get(name=oname)
        non_senator_offices += list(off.get_descendants(include_self=True))

    print("Filtering {} different offices.".format(len(non_senator_offices)))

    now = datetime.datetime.now()
    date = now.strftime("%d_%B_%Y")
    log_fname = "senator_data_log-{}.csv".format(date)

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
                "log"
            ],
            dialect='excel',
            delimiter=",",
            extrasaction='ignore')
        csv_log.writeheader()

        add_non_senator_officials(
            csv_log,
            status_type,
            sec_source,
            non_senator_offices)

        add_senator_only_postassertions(
            csv_log,
            status_type,
            sec_source,
            non_senator_offices)

    print("Wrote {}".format(log_fname))


def add_senator_only_postassertions(csv_log,
                                    status_type,
                                    sec_source,
                                    non_senator_offices):

    senator_offices = Office.objects.get(
        name='senator').get_descendants(include_self=True)

    # If a person is listed with a senator post assertion but none of
    #   the other offices in the list, then create a senator status assertion
    #   with the same start and end date as the existing senator post assertion
    only_senators = Person.objects.filter(
        post_assertions__office__in=senator_offices
    ).exclude(post_assertions__office__in=non_senator_offices,)

    for person in only_senators:
        sa = StatusAssertion(
            person=person,
            status=status_type,
            secondary_source=sec_source,
        )

        # dates; need
        sen_postassertions = person.post_assertions.order_by('date_start')

        date_start = sen_postassertions.first().date_start
        date_end = sen_postassertions.last().date_end
        sa.date_start = date_start
        sa.date_end = date_end
        sa.save()

        log_dict = {
            'person': person.id,
            'statusassertion': sa.id,
            'date_start': date_start,
            'date_end': date_end,
            'log': 'senator, no other offices held'
        }

        csv_log.writerow(log_dict)

    print("OSEN {}".format(only_senators.count()))


def add_non_senator_officials(csv_log,
                              status_type,
                              sec_source,
                              non_senator_offices):

    # This process affects each person who has a post assertion with a start
    # date after -180, for the following offices - quaestor, tribunis plebis,
    # aedilis (and subtypes), praetor (and subtypes), consul (and subtypes),
    # censor (and subtypes), princeps senatus and senator including the
    # different subtypes - senator quaestorius, praetorius consularis etc)

    # If a person has post assertion as listed above except senator and its
    # subtypes, then create a senator status assertion

    print non_senator_offices

    person_list = Person.objects.filter(
        post_assertions__office__in=non_senator_offices,
        post_assertions__date_start__gte=-180
    ).distinct()

    print("Will add {} new Senator Status Assertions".format(len(person_list)))

    # create Senator StatusAssertions

    for person in person_list:
        log_msg = "No senator post assertions; "

        sa = StatusAssertion(
            person=person,
            status=status_type,
            secondary_source=sec_source)

        sa.save()

        date_start, date_start_uncertain, msg = compute_start_date(person)
        log_msg += msg

        date_end, date_end_uncertain, msg = compute_end_date(person)
        log_msg += msg

        log_dict = {
            'person': person.id,
            'statusassertion': sa.id,
            'date_start': date_start,
            'date_start_uncertain': date_start_uncertain,
            'date_end': date_end,
            'date_end_uncertain': date_end_uncertain,
            'log': log_msg
        }

        csv_log.writerow(log_dict)


def compute_start_date(person):
    """ Given a person, returns the start date and the uncertian flag
    """
    log_message = ""

    date_start = None
    uncertain = None

    aed_list = [o.name for o in Office.objects.get(
        name="aedilis").get_descendants(include_self=True)]

    pra_list = [o.name for o in Office.objects.get(
        name="praetor").get_descendants(include_self=True)]

    con_list = [o.name for o in Office.objects.get(
        name="consul").get_descendants(include_self=True)]

    tri_list = [o.name for o in Office.objects.get(
        name="tribunus plebis").get_descendants(include_self=True)]

    other_offices_list = aed_list + pra_list + con_list + tri_list

    # quaestors
    qua_pa_list = PostAssertion.objects.filter(
        person=person,
        office__name='quaestor',
        date_start__gte=-180).order_by('date_start')

    # Eques Status Assertion end date
    #   If senator status assertion has been created and a status assertion
    #   of eques already exists, set the end date of the eques status assertion
    #   to the year before the start date of the new senator status assertion.

    log_message = "date_start: "

    # If person has a quaestor post assertion, then set the start date of the
    # senator post assertion = quaestor start date + 1, certainty = certain.
    if qua_pa_list.exists():
        date_start = qua_pa_list.first().date_start
        uncertain = False
        log_message += "quaestor; "
    else:
        pa_list = PostAssertion.objects.filter(
            person=person,
            office__name__in=other_offices_list,
            date_start__gte=-180).order_by('date_start')

        if pa_list.exists():
            # if the person has no quaestor post assertion
            office_name = pa_list.first().office.name
            log_message += "{}; ".format(office_name)

            if office_name in aed_list:
                # earliest postassertion is aedile (and subtypes)
                # start date of the senator post assertion is the start date of
                # the aedileship - 2, certainty = uncertain

                date_start = pa_list.first().date_start - 2
                uncertain = True

            elif office_name in tri_list:
                # earliest post assertion is tribune of the plebs and subtypes
                # start date of the senator status assertion to the start
                # date of the tribunate of the plebs,
                # certainty = the same as the post assertion

                date_start = pa_list.first().date_start
                uncertain = pa_list.first().date_start_uncertain

            elif office_name in pra_list:
                # earliest postassertion is praetor (and subtypes)
                # start date of the senator post assertion is the start date of
                # the praetorship - 2, certainty = uncertain

                date_start = pa_list.first().date_start - 2
                uncertain = True
            else:
                # earliest post assertion is consul (and subtypes)
                # start date of the senator post assertion to the start date of
                # the consulship - 5, certainty = uncertain

                date_start = pa_list.first().date_start - 5
                uncertain = True

    return date_start, uncertain, log_message


def compute_end_date(person):
    #   The only time we can be sure that a person is no longer a senator
    #   is when they are dead (all types !!), exiled or expelled.)

    date_end = None
    uncertain = None

    date_types = ["death", "death - natural", "death - violent",
                  "exile", "expelled from Senate", "extradited",
                  "proscribed"]

    dates = person.dateinformation_set.filter(
        date_type__name__in=date_types).order_by('value')

    log_message = "date_end: "

    if dates.exists():
        # If the person has a life date of expelled or exiled or death or
        #   death - violent, set the end date of the senator status assertion
        #   to the earliest of these life dates, certainty = the same
        #   certainty as the life date
        date_end = dates.first().value
        uncertain = dates.first().uncertain
        log_message += "{}; ".format(dates.first().date_type.name)

    else:
        # Otherwise set end date to the end date of the last known office
        pa_list = person.post_assertions.filter()
        if pa_list.exists():
            pa = pa_list.order_by('-date_end').first()
            date_end = pa.date_end
            uncertain = True
            log_message = "last known office; "

    return date_end, uncertain, log_message
