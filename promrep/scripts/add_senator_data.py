# -*- coding: utf-8 -*-

# this script enriches the database with the Senator StatusAssertions
#   for full rules and dicussion please see the original JIRA ticket here:
#   https://jira.dighum.kcl.ac.uk/projects/DPRR/issues/DPRR-256


from promrep.models import (
    Office, Person, PostAssertion, SecondarySource, StatusAssertion,
    StatusType
)


def run():
    print("Adding Senator Status Assertions")

    add_simple_senators()


def add_simple_senators():
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

    status_type = StatusType.objects.get_or_create(name="senator")
    sec_source = SecondarySource.objects.get_or_create(name="DPRR Team")

    for person in person_list:
        sa = StatusAssertion.objects.new(
            person=person,
            status=status_type,
            secondary_source=sec_source)

        print("Created new Status Assertion {}".format(sa))

        date_start, uncertain = compute_start_date(person)


def compute_start_date(person):
    """ Given a person, returns the start date and the uncertian flag
    """

    date_start = None
    certain = True

    pa_list = PostAssertion.objects.filter(
        person=person,
        office__name='quaestor',
        date_start__gte=-180)  # .order_by('year_start')

    # If person has a quaestor post assertion, then set the start date of the
    # senator post assertion = quaestor start date + 1, certainty = certain.
    if pa_list.exists():
        date_start = pa_list.first().date_start
        print(date_start)

    """
    If the person has no quaestor post assertion, then set the start date
      according to the following rules:
    * If the earliest post assertion is for an office of aedile (and subtypes)
     set the start date of the senator post assertion to the start date of
     the aedileship - 2, certainty = uncertain
    * If the earliest post assertion is for an office of praetor (and subtypes)
     set the start date of the senator post assertion to the start date of
     the praetorship - 2, certainty = uncertain
     * If the earliest post assertion is for an office of consul (and subtypes)
     set the start date of the senator post assertion to the start date of
     the consulship - 5, certainty = uncertain
    """

    return date_start, certain
