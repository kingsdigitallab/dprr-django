from django.test import TestCase
from promrep.models import Praenomen, Tribe, Person

class PersonTest(TestCase):

    def create_person(self,
        praenomen = Praenomen.objects.get(abbrev="M."),
        nomen = "Antonius",
        re_number="28",
        cognomen=""):

        return Person.objects.create(nomen=nomen, re_number=re_number, praenomen = praenomen)

    def test_person_creation(self):
        p = self.create_person()

        self.assertTrue(isinstance(p, Person))
        self.assertEqual(p.__unicode__(), p.praenomen.abbrev + ' ' + p.nomen + ' (' + p.re_number + ')')

    def test_person_update(self):
        p1 = self.create_person()
        p2 = Person(nomen=p1.nomen, re_number=p1.re_number, praenomen = p1.praenomen, cognomen="Arius")

        p1.update_empty_fields(p2)

        self.assertEqual(p1.cognomen, p2.cognomen)







