#!/usr/bin/python
# -*- coding: utf-8 -*-

# data import auxiliary functions

from promrep.models import Assertion, AssertionPerson, AssertionType, \
    Certainty, Date, DateType, Office, Person, Praenomen, \
    PrimarySource, RoleType, SecondarySource, Sex


def is_new_person(person):

    print 'is_new_person ',

    identic_persons = \
        Person.objects.filter(real_number=person.real_number,
                              nomen=person.nomen)

    if identic_persons.count() == 1:

        # should print the debug information
        diffs = person.compare(identic_persons[0])
        print "[SAME_PERSON] Parsing person already in database:",

        diff_keys = diffs[0].keys()
        if len(diff_keys) == 0:
            print "No new info."
        else:
            print "Different information: printing diffs:"

        for key in diff_keys:
            print key, '[SAME_PERSON]\tOld:', diffs[1][key], 'New:', diffs[0][key]

        person = identic_persons[0]
        print '[SAME_PERSON] Keeping previous (id=' + str(person.id)  + ') in database... '

        return False
    elif identic_persons.count() > 1:
        print 'MANY'
        return None
    else:
        print 'None'
        return True


def add_new_person_to_db(person):
    new_person = is_new_person(person)

    if new_person == True:
        try:
            print "[DEBUG] " + person.original_text
            person.save()
            print '[NEW PERSON] Saved person ' + str(person) \
                + ' with id: ' + str(person.id)

            return True

        except Exception, e:
            print e
            return False

        print '[NEW PERSON] ' + person.original_text

    elif new_person == False:
        print '[HITS DATABASE] ' + person.original_text
        return None
    else:
        print '[ERROR: Multiple persons with same identifier] ' + person.original_text
        return False

