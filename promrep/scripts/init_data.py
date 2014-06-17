#!/usr/bin/python
# -*- coding: utf-8 -*-

# initial data for the promrep app

from django.core.management import call_command


def run():
    print 'Loading initial data fixtures'

    print 'Loading Sex Data...'
    call_command('loaddata', 'promrep/fixtures/promrep_sex.json')

    print 'Loading Praenomen Data...'
    call_command('loaddata', 'promrep/fixtures/promrep_praenomina.json')

    print 'Loading Office Data...'
    call_command('loaddata', 'promrep/fixtures/promrep_offices.json')

    print 'Loading Certainty Data...'
    call_command('loaddata', 'promrep/fixtures/promrep_certainty.json')

    print 'Loading Role Types...'
    call_command('loaddata', 'promrep/fixtures/promrep_roletype.json')

    print 'Loading Assertion Types...'
    call_command('loaddata', 'promrep/fixtures/promrep_assertiontype.json')

    print 'Loading Secondary Sources...'
    call_command('loaddata', 'promrep/fixtures/promrep_secondarysource.json')

    print 'Loading Relationship Data...'
    call_command('loaddata', 'promrep/fixtures/promrep_relationship.json')