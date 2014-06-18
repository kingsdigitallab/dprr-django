from django.test import TestCase
from promrep.models import Date

import add_brennan_data as brennan

class AddBrennanDataTestCase(TestCase):

    def test_parse_date(self):

        self.assertEqual(brennan.parse_brennan_date('50').year, 50)

        mydate = brennan.parse_brennan_date('before 60')
        self.assertEqual(mydate.year, 60)

        mydate = brennan.parse_brennan_date('?before 60')

        self.assertEqual(mydate.year, 60)
        self.assertEqual(mydate.year_uncertain, True)


        mydate = brennan.parse_brennan_date('??before 50')
        self.assertEqual(mydate.year, 50)
        self.assertEqual(mydate.year_uncertain, True)

        mydate = brennan.parse_brennan_date('?by 50')
        self.assertEqual(mydate.year, 50)
        self.assertEqual(mydate.year_uncertain, True)
        self.assertEqual(mydate.circa, True)

        mydate = brennan.parse_brennan_date('??ca. 70')

        self.assertEqual(mydate.year, 70)
        self.assertEqual(mydate.year_uncertain, True)
        self.assertEqual(mydate.circa, True)
