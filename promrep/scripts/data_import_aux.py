#!/usr/bin/python
# -*- coding: utf-8 -*-

# data import auxiliary functions

from promrep.models import Assertion, AssertionPerson, AssertionType, \
    Certainty, Date, DateType, Office, Person, Praenomen, \
    PrimarySource, RoleType, SecondarySource, Sex

def is_new_person(person):

    print "is_new_person ",

    identic_persons = Person.objects.filter(real_number=person.real_number, nomen=person.nomen)

    if identic_persons.count() == 1:
        print "ONE"
        person = identic_persons[0]
        return False
    elif identic_persons.count() > 1:
        print "MANY"
        return None
    else:
        print "None"
        return True
