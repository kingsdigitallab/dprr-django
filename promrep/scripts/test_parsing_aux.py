from promrep.models import Praenomen, Tribe
from django.test import TestCase

import parsing_aux as aux

class AddParsingAuxTestCase(TestCase):
    fixtures = ['promrep_sex.json', 'promrep_praenomina.json', 'promrep_tribe.json', ]

    def test_parse_names(self):

        # for now let's just expect a None
        p = aux.parse_person("Err. Antonius M. f. M. n. (28)")
        self.assertEqual(p, None)

        # when the praenomen is "-"
        p = aux.parse_person("- Antonius M. f. M. n. (28)")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="-"))
        self.assertEqual(p.nomen, "Antonius")
        self.assertEqual(p.filiation, "M. f. M. n.")
        self.assertEqual(p.real_number, "28")

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



    def test_parse_brennan_persons(self):

        p = aux.parse_brennan_person("M. Furius (44) Camillus")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="M."))
        self.assertEqual(p.nomen, "Furius")
        self.assertEqual(p.real_number, "44")
        self.assertEqual(p.cognomen, "Camillus")
        self.assertFalse(p.patrician)

        p = aux.parse_brennan_person("L. Plautius (*5, 33) Venox")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="L."))
        self.assertEqual(p.nomen, "Plautius")
        self.assertEqual(p.real_number, "*5, 33")
        self.assertEqual(p.cognomen, "Venox")
        self.assertFalse(p.patrician)

        p = aux.parse_brennan_person("L. Postumius (*19) Megellus")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="L."))
        self.assertEqual(p.nomen, "Postumius")
        self.assertEqual(p.real_number, "*19")
        self.assertEqual(p.cognomen, "Megellus")
        self.assertFalse(p.patrician)

        p = aux.parse_brennan_person("M. Pomponius (*6) Matho")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="M."))
        self.assertEqual(p.nomen, "Pomponius")
        self.assertEqual(p.real_number, "*6")
        self.assertEqual(p.cognomen, "Matho")
        self.assertFalse(p.patrician)

        p = aux.parse_brennan_person("M'. Pomponius (*5) Matho")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="M'."))
        self.assertEqual(p.nomen, "Pomponius")
        self.assertEqual(p.real_number, "*5")
        self.assertEqual(p.cognomen, "Matho")
        self.assertFalse(p.patrician)

        p = aux.parse_brennan_person("M. Valerius (*31)")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="M."))
        self.assertEqual(p.nomen, "Valerius")
        self.assertEqual(p.real_number, "*31")
        self.assertFalse(p.patrician)

        p = aux.parse_brennan_person("T. Quinctius (Cin. *12) Crispinus")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="T."))
        self.assertEqual(p.nomen, "Quinctius")
        self.assertEqual(p.real_number, "Cin. *12")
        self.assertEqual(p.cognomen, "Crispinus")
        self.assertFalse(p.patrician)

        p = aux.parse_brennan_person("K. Quinctius (Claudius 151) Claudus Flamininus")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="K."))
        self.assertEqual(p.nomen, "Quinctius")
        self.assertEqual(p.real_number, "Claudius 151")
        self.assertEqual(p.cognomen, "Claudus")
        self.assertEqual(p.other_names, "Flamininus")
        self.assertFalse(p.patrician)

        p = aux.parse_brennan_person("L. Acilius (Atilius 16 = Acilius 7) (Sapiens)")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="L."))
        self.assertEqual(p.nomen, "Acilius")
        self.assertEqual(p.real_number, "Atilius 16 = Acilius 7")
        self.assertEqual(p.cognomen, "(Sapiens)")
        self.assertFalse(p.patrician)

        p = aux.parse_brennan_person("Sex. Iulius (148/149) Caesar")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="Sex."))
        self.assertEqual(p.nomen, "Iulius")
        self.assertEqual(p.real_number, "148/149")
        self.assertEqual(p.cognomen, "Caesar")
        self.assertFalse(p.patrician)

        p = aux.parse_brennan_person("Q. Marcius")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="Q."))
        self.assertEqual(p.nomen, "Marcius")
        self.assertFalse(p.patrician)

        p = aux.parse_brennan_person("C. Claudius (246) Nero")
        self.assertEqual(p.praenomen, Praenomen.objects.get(abbrev="C."))
        self.assertEqual(p.nomen, "Claudius")
        self.assertEqual(p.real_number, "246")
        self.assertEqual(p.cognomen, "Nero")
        self.assertFalse(p.patrician)


