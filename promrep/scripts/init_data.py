#!/usr/bin/python
# -*- coding: utf-8 -*-

# initial data for the promrep app

from django.core.management import call_command

def run():
    print 'Loading initial data fixtures'

    print '  Sex...'
    call_command('loaddata', 'promrep/fixtures/promrep_sex.json')

    print '  Praenomen...'
    call_command('loaddata', 'promrep/fixtures/promrep_praenomina.json')

    print '  Gens...'
    call_command('loaddata', 'promrep/fixtures/promrep_gens.json')

    print '  Office...'
    call_command('loaddata', 'promrep/fixtures/promrep_offices.json')

    print '  Role Types...'
    call_command('loaddata', 'promrep/fixtures/promrep_roletype.json')

    print '  Assertion Types...'
    call_command('loaddata', 'promrep/fixtures/promrep_assertiontype.json')

    print '  Secondary Sources...'
    call_command('loaddata', 'promrep/fixtures/promrep_secondarysource.json')

    print '  Relationship Data...'
    call_command('loaddata', 'promrep/fixtures/promrep_relationship.json')

    print '  Tribe Data...'
    call_command('loaddata', 'promrep/fixtures/promrep_tribe.json')