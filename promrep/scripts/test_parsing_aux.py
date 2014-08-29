from promrep.models import Praenomen
from django.test import TestCase

import parsing_aux as aux

class AddParsingAuxTestCase(TestCase):
    fixtures = ['promrep_sex.json', 'promrep_praenomina.json']

    def test_parse_date(self):

        p = aux.parse_person("M. Antonius M. f. M. n. (28)")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="M."))
        self.assertEqual(p.nomen, "Antonius")
        self.assertEqual(p.filiation, "M. f. M. n.")
        self.assertEqual(p.real_number, "28")

        p = aux.parse_person("L. Appuleius Saturninus (29)")
        self.assertEqual(p.nomen, "Appuleius")
        self.assertEqual(p.cognomen, "Saturninus")
        self.assertEqual(p.real_number, "29")

        p = aux.parse_person("T. Diditus (5)")
        self.assertEqual(p.nomen, "Diditus")
        self.assertEqual(p.real_number, "5")
        self.assertFalse(p.patrician)

        p = aux.parse_person("C. Claudius Pulcher Pat. (302)")
        self.assertEqual(p.nomen, "Claudius")
        self.assertTrue(p.patrician)
        self.assertTrue(p.patrician_certainty)
        self.assertEqual(p.real_number, "302")

        p = aux.parse_person("C. M[amilius? - f. Limetanus?] (7)")
        self.assertEqual(p.nomen, "M[amilius?")
        self.assertEqual(p.real_number, "7")


