from promrep.models import Date
from django.test import TestCase
import add_brennan_data as brennan

class AddBrennanDataTestCase(TestCase):

    def test_parse_date(self):

        # self.assertEqual(brennan.parse_brennan_date('50').year, 50)

        mydate_list = brennan.parse_brennan_date('before 60')
        self.assertEqual(len(mydate_list), 1)

        mydate = mydate_list[0]
        self.assertEqual(mydate.interval, Date.DATE_MAX)
        self.assertEqual(mydate.year, 60)

        mydate_list = brennan.parse_brennan_date('?before 60')
        self.assertEqual(len(mydate_list), 1)
        self.assertEqual(mydate_list[0].interval, Date.DATE_MAX)
        self.assertEqual(mydate_list[0].year, 60)
        self.assertEqual(mydate_list[0].year_uncertain, True)


        mydate_list = brennan.parse_brennan_date('??before 50')
        self.assertEqual(len(mydate_list), 1)
        mydate = mydate_list[0]
        self.assertEqual(mydate.year, 50)
        self.assertEqual(mydate.year_uncertain, True)

        mydate_list = brennan.parse_brennan_date('?by 50')
        self.assertEqual(len(mydate_list), 1)
        mydate = mydate_list[0]
        self.assertEqual(mydate.year, 50)
        self.assertEqual(mydate.year_uncertain, True)
        self.assertEqual(mydate.circa, True)


        mydate_list = brennan.parse_brennan_date('??ca. 70')
        self.assertEqual(len(mydate_list), 1)
        mydate = mydate_list[0]
        self.assertEqual(mydate.year, 70)
        self.assertEqual(mydate.year_uncertain, True)
        self.assertEqual(mydate.circa, True)

        mydate_list = brennan.parse_brennan_date('?before ca. 115')
        self.assertEqual(len(mydate_list), 1)
        mydate = mydate_list[0]
        self.assertEqual(mydate.year, 115)
        self.assertEqual(mydate.year_uncertain, True)
        self.assertEqual(mydate.circa, True)
        self.assertEqual(mydate.interval, Date.DATE_MAX)



