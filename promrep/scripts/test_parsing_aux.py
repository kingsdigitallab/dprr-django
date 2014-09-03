from promrep.models import Praenomen, Tribe
from django.test import TestCase

import parsing_aux as aux

class AddParsingAuxTestCase(TestCase):
    fixtures = ['promrep_sex.json', 'promrep_praenomina.json', 'promrep_tribe.json', ]

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
        ######### date (up to taht year, including)

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

        ### tribe
        p = aux.parse_person("C. Claudius C. f. Arn. Glaber (165)")
        self.assertEqual(p.nomen, "Claudius")
        self.assertEqual(p.tribe, Tribe.objects.get(abbrev="Arn."))
        self.assertEqual(p.cognomen, "Glaber")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="C."))
        self.assertEqual(p.real_number, "165")

        p = aux.parse_person("M. Pupius Piso Frugi Calpurnianus (*2.100)")
        self.assertEqual(p.nomen, "Pupius")
        self.assertEqual(p.cognomen, "Piso")
        self.assertEqual(p.other_names, "Frugi Calpurnianus")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="M."))
        self.assertEqual(p.real_number, "*2.100")

        # TODO: extra date info...
        p = aux.parse_person("88 or 80-40: L. Iulius Caesar Pat. (143)")
        self.assertEqual(p.nomen, "Iulius")
        self.assertEqual(p.cognomen, "Caesar")
        self.assertEqual(p.other_names, "")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="L."))
        self.assertEqual(p.real_number, "143")
        self.assertTrue(p.patrician)

        p = aux.parse_person("Before 47-ca. 40: P. Servilius Isauricus (67)")
        self.assertEqual(p.nomen, "Servilius")
        self.assertEqual(p.cognomen, "Isauricus")
        self.assertEqual(p.other_names, "")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="P."))
        self.assertEqual(p.real_number, "67")
        self.assertFalse(p.patrician)

        p = aux.parse_person("Ca. 45-43: A. Hirtius (2)")
        self.assertEqual(p.nomen, "Hirtius")
        self.assertEqual(p.cognomen, "")
        self.assertEqual(p.other_names, "")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="A."))
        self.assertEqual(p.real_number, "2")
        self.assertFalse(p.patrician)


        # p = aux.parse_person("C. M[amilius? - f. Limetanus?] (7)")
        # self.assertEqual(p.nomen, "M[amilius?")
        # self.assertEqual(p.real_number, "7")


