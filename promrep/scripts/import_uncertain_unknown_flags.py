import os

import unicodecsv as csv
from django.core.exceptions import ObjectDoesNotExist
from promrep.models import Person, PostAssertion


def run():
    try:
        file_name = "promrep/scripts/data/AddUncertainFlagV1.csv"
        file_path = os.path.abspath(file_name)

        csv_file = open(file_path)
        csv_dict = csv.DictReader(csv_file)

        for row in csv_dict:
            person_id = row["person_id"]
            try:
                person = Person.objects.get(id=person_id)
                person.uncertain = True
                person.save()
            except ObjectDoesNotExist:
                print(("Person with ID {} not found.".format(person_id)))

            post_id = row["post_id"]
            try:
                post = PostAssertion.objects.get(id=post_id)
                post.unknown = True
                post.save()
            except ObjectDoesNotExist:
                print(("PostAssertion with ID {} not found.".format(post_id)))
    except IOError:
        print(("Uncertain/unknown flags file not found: {}".format(file_name)))
