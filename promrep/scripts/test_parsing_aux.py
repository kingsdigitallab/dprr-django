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
        self.assertEqual(p.filiation, "")
        self.assertEqual(p.nomen, "Appuleius")
        self.assertEqual(p.cognomen, "Saturninus")
        self.assertEqual(p.real_number, "29")

        p = aux.parse_person("T. Diditus (5)")
        self.assertEqual(p.nomen, "Diditus")
        self.assertEqual(p.filiation, "")
        self.assertEqual(p.cognomen, "")
        self.assertEqual(p.real_number, "5")
        self.assertFalse(p.patrician)

        p = aux.parse_person("C. Claudius Pulcher Pat. (302)")
        self.assertEqual(p.nomen, "Claudius")
        self.assertEqual(p.filiation, "")
        self.assertTrue(p.patrician)
        self.assertTrue(p.patrician_certainty)
        self.assertEqual(p.real_number, "302")

        # uncertain praenomen, patrician
        p= aux.parse_person("A.? Manlius Torquatus Pat. (76)")
        self.assertEqual(p.nomen, "Manlius")
        self.assertEqual(p.filiation, "")
        self.assertTrue(p.patrician)
        self.assertTrue(p.patrician_certainty)
        self.assertEqual(p.real_number, "76")

        # uncertain praenomen
        p= aux.parse_person("C.? Memmius (7)")
        self.assertEqual(p.nomen, "Memmius")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="C."))
        self.assertFalse(p.praenomen_certainty)
        self.assertEqual(p.real_number, "7")

        ### TODO: date/office uncertainty ??
        p= aux.parse_person("? C. Memmius (7)")
        self.assertEqual(p.nomen, "Memmius")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="C."))
        self.assertTrue(p.praenomen_certainty)
        self.assertEqual(p.real_number, "7")

        p = aux.parse_person("L.? Novius Niger (12, cf. 7)")
        self.assertEqual(p.nomen, "Novius")
        self.assertEqual(p.cognomen, "Niger")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="L."))
        self.assertFalse(p.praenomen_certainty)
        self.assertEqual(p.real_number, "12, cf. 7")

        ### TODO: cognomen abbrev ??
        p = aux.parse_person("C. Claudius C. f. Arn. Glaber (165)")
        self.assertEqual(p.nomen, "Claudius")
        self.assertEqual(p.cognomen, "Arn.")
        self.assertEqual(p.other_names, "Glaber")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="C."))
        self.assertEqual(p.real_number, "165")

        p = aux.parse_person("M. Pupius Piso Frugi Calpurnianus (*2.100)")
        self.assertEqual(p.nomen, "Pupius")
        self.assertEqual(p.cognomen, "Piso")
        self.assertEqual(p.other_names, "Frugi Calpurnianus")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="M."))
        self.assertEqual(p.real_number, "*2.100")


        # p = aux.parse_person("C. M[amilius? - f. Limetanus?] (7)")
        # self.assertEqual(p.nomen, "M[amilius?")
        # self.assertEqual(p.real_number, "7")

