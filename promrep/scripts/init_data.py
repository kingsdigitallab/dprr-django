# initial data for the promrep app

from django.core.management import call_command

def run():
    print "Loading initial data fixtures"

    print "Loading Sex Data..."
    call_command("loaddata", "promrep/fixtures/promrep_sex.json")

    print "Loading Praenomen Data..."
    call_command("loaddata", "promrep/fixtures/promrep_praenomina.json")

    print "Loading Office Data..."
    call_command("loaddata", "promrep/fixtures/promrep_offices.json")

    print "Loading Certainty Data..."
    call_command("loaddata", "promrep/fixtures/promrep_certainty.json")