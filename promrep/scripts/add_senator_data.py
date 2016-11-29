# -*- coding: utf-8 -*-

# this script enriches the database with the Senator StatusAssertions
#   for full rules and dicussion please see the original JIRA ticket here:
#   https://jira.dighum.kcl.ac.uk/projects/DPRR/issues/DPRR-256


from promrep.models import (
    Office, Person, PostAssertion, SecondarySource, StatusAssertion,
    StatusType
)

import csv


def run():
    print("Adding Senator Status Assertions")

    add_simple_senators()


def add_simple_senators():

    log_fname = "senator_data.log"

    csv_log = csv.DictWriter(
        open(log_fname, 'wb'),
        ["person", "statusassertion"],
        dialect='excel',
        delimiter=",",
        extrasaction='ignore')
    csv_log.writeheader()

    # This process affects each person who has a post assertion with a start
    # date after -180, for the following offices - quaestor, tribunis plebis,
    # aedilis (and subtypes), praetor (and subtypes), consul (and subtypes),
    # censor (and subtypes), princeps senatus and senator including the
    # different subtypes - senator quaestorius, praetorius consularis etc)

    # If a person has post assertion as listed above except senator and its
    # subtypes, then create a senator status assertion

    office_list = ['quaestor', 'tribunus plebis', 'aedilis',
                   'praetor', 'consul', 'censor', 'princeps senatus',
                   'senator']

    all_offices = []

    for oname in office_list:
        off = Office.objects.get(name=oname)
        all_offices += list(off.get_descendants(include_self=True))

    print("Filtering {} different offices.".format(len(all_offices)))

    print all_offices

    person_list = Person.objects.filter(
        post_assertions__office__in=all_offices,
        post_assertions__date_start__gte=-180
    ).exclude(
        post_assertions__office=Office.objects.get(name='senator')
    ).distinct()

    print("Will add {} new Senator Status Assertions".format(len(person_list)))

    # create Senator StatusAssertions

    status_type, created = StatusType.objects.get_or_create(name="senator")
    sec_source, created = SecondarySource.objects.get_or_create(
        name="DPRR Team")

    for person in person_list:
        sa = StatusAssertion(
            person=person,
            status=status_type,
            secondary_source=sec_source)

        print("Created new Status Assertion {}".format(sa))

        date_start, uncertain = compute_start_date(person)
        date_end, uncertain = compute_end_date(person, all_offices)


def compute_start_date(person):
    """ Given a person, returns the start date and the uncertian flag
    """

    date_start = None
    uncertain = None

    aed_list = [o.name for o in Office.objects.get(
        name="aedilis").get_descendants(include_self=True)]
    pra_list = [o.name for o in Office.objects.get(
        name="praetor").get_descendants(include_self=True)]
    con_list = [o.name for o in Office.objects.get(
        name="consul").get_descendants(include_self=True)]

    other_offices_list = aed_list + pra_list + con_list

    # quaestors
    pa_list = PostAssertion.objects.filter(
        person=person,
        office__name='quaestor',
        date_start__gte=-180).order_by('date_start')

    # If person has a quaestor post assertion, then set the start date of the
    # senator post assertion = quaestor start date + 1, certainty = certain.
    if pa_list.exists():
        date_start = pa_list.first().date_start
        uncertain = False
        print(date_start)
    else:
        pa_list = PostAssertion.objects.filter(
            person=person,
            office__name__in=other_offices_list,
            date_start__gte=-180).order_by('date_start')

        if pa_list.exists():
            # if the person has no quaestor post assertion

            if pa_list.first().office in aed_list:
                # earliest postassertion is aedile (and subtypes)
                # start date of the senator post assertion is the start date of
                # the aedileship - 2, certainty = uncertain

                date_start = pa_list.first().date_start - 2
                uncertain = True

            elif pa_list.first().office in pra_list:
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

    return date_start, uncertain


def compute_end_date(person, all_offices_list):
    #   The only time we can be sure that a person is no longer a senator
    #   is when they are dead (all types !!), exiled or expelled.)

    date_end = None
    uncertain = None

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
        date_end = dates.first().value
        uncertain = dates.first().uncertain

    else:
        # Otherwise set end date to the latest end date of any of the offices
        #   listed above including senator and subtypes, certainty = uncertain
        pa_list = person.post_assertions.filter(
            office__name__in=all_offices_list)
        if pa_list.exists():
            pa = pa_list.order_by('-date_end').first()
            date_end = pa.date_end
            uncertain = True

    return date_end, uncertain
