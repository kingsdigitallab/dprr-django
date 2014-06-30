from promrep.models import Date
from django.test import TestCase
import add_brennan_data as brennan

class AddBrennanDataTestCase(TestCase):

    def test_parse_date(self):

        mydate = brennan.parse_brennan_date('55')
        self.assertEqual(mydate[0].interval, Date.DATE_MIN)
        self.assertEqual(mydate[0].year, -55)
        self.assertEqual(mydate[0].year_uncertain, False)

        self.assertEqual(mydate[1].interval, Date.DATE_MAX)
        self.assertEqual(mydate[1].year, -54)
        self.assertEqual(mydate[1].year_uncertain, False)

        mydate = brennan.parse_brennan_date('before 60')
        self.assertEqual(mydate[1], None)
        self.assertEqual(mydate[0].interval, Date.DATE_MAX)
        self.assertEqual(mydate[0].year, -61)

        mydate = brennan.parse_brennan_date('?before 60')
        self.assertEqual(mydate[1], None)
        self.assertEqual(mydate[0].interval, Date.DATE_MAX)
        self.assertEqual(mydate[0].year, -61)
        self.assertEqual(mydate[0].year_uncertain, True)

        mydate = brennan.parse_brennan_date('??before 60')
        self.assertEqual(mydate[1], None)
        self.assertEqual(mydate[0].interval, Date.DATE_MAX)
        self.assertEqual(mydate[0].year, -61)
        self.assertEqual(mydate[0].year_uncertain, True)

        mydate = brennan.parse_brennan_date('?by 50')
        self.assertEqual(mydate[1], None)
        self.assertEqual(mydate[0].year, -50)
        self.assertEqual(mydate[0].year_uncertain, True)
        self.assertEqual(mydate[0].circa, False)


        mydate = brennan.parse_brennan_date('??ca. 70')
        self.assertEqual(mydate[1], None)
        self.assertEqual(mydate[0].year, -70)
        self.assertEqual(mydate[0].year_uncertain, True)
        self.assertEqual(mydate[0].circa, True)

        mydate = brennan.parse_brennan_date('?before ca. 115')

        self.assertEqual(mydate[1], None)
        self.assertEqual(mydate[0].year, -116)
        self.assertEqual(mydate[0].year_uncertain, True)
        self.assertEqual(mydate[0].circa, True)
        self.assertEqual(mydate[0].interval, Date.DATE_MAX)


        mydate = brennan.parse_brennan_date('3c')
        self.assertEqual(mydate[0].year, -300)
        self.assertEqual(mydate[1].year, -201)
        self.assertEqual(mydate[0].interval, Date.DATE_MIN)
        self.assertEqual(mydate[1].interval, Date.DATE_MAX)


        mydate = brennan.parse_brennan_date('3 or 2c')
        self.assertEqual(mydate[0].year, -300)
        self.assertEqual(mydate[1].year, -101)
        self.assertEqual(mydate[0].interval, Date.DATE_MIN)
        self.assertEqual(mydate[1].interval, Date.DATE_MAX)


        mydate = brennan.parse_brennan_date('3/2c')
        self.assertEqual(mydate[0].year, -300)
        self.assertEqual(mydate[1].year, -101)
        self.assertEqual(mydate[0].interval, Date.DATE_MIN)
        self.assertEqual(mydate[1].interval, Date.DATE_MAX)
