#!/usr/bin/python
# -*- coding: utf-8 -*-

# data import auxiliary functions

from promrep.models import Assertion, AssertionPerson, AssertionType, \
    Certainty, Date, DateType, Office, Person, Praenomen, \
    PrimarySource, RoleType, SecondarySource, Sex


def add_person_to_db(person):
    """Returns a tuple with the status and id of the person"""

    # tests if there are more persons with the same identifier (nomen + real)
    identic = \
        Person.objects.filter(real_number=person.real_number,
                              nomen=person.nomen)

    if identic.count() == 1:
        existing_person = identic[0]
        # should print the debug information
        diffs = existing_person.compare(person)
        print "[SAME_PERSON] Parsing person already in database:",

        diff_keys = diffs[0].keys()
        if len(diff_keys) == 0:
            print "No new info."
        else:
            print "printing diffs:"

        for key in diff_keys:
            print '[SAME_PERSON]', key, 'Old:', diffs[0][key], 'New:', diffs[1][key]

        print '[SAME_PERSON] Keeping previous (id=' + str(existing_person.id)  + ') in database... '

        return (False, existing_person.id)

    elif identic.count() > 1:
        # todo: print a verbose error
        print '[ERROR] More than one person matches query... not adding person to db.'
        return (None, None)
    else:
        try:
            person.save()
            print "[DEBUG] saved person with id", person.id
            return (True, person.id)

        except:
            print '[ERROR] Unable to save person in the database.'
            return (None, None)


