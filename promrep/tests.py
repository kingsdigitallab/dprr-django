from django.test import TestCase
from promrep.models import Praenomen, Tribe, Person

class PersonTest(TestCase):

    def create_person(self,
        praenomen = Praenomen.objects.get(abbrev="M."),
        nomen = "Antonius",
        real_number="28",
        cognomen=""):

        return Person.objects.create(nomen=nomen, real_number=real_number, praenomen = praenomen)

    def test_person_creation(self):
        p = self.create_person()

        self.assertTrue(isinstance(p, Person))
        self.assertEqual(p.__unicode__(), p.praenomen.abbrev + ' ' + p.nomen + ' (' + p.real_number + ')')



        # p2 = self.create_person(cognomen="Arius")

