from django.test import TestCase
from promrep.models import Person


class PersonTest(TestCase):

    def setUp(self):
        self.filiations = [
            {'text': None, 'f': None, 'n': None},
            {'text': '', 'f': None, 'n': None},
            {'text': 'ABC', 'f': None, 'n': None},
            {'text': 'A. f.', 'f': 'A.', 'n': None},
            {'text': 'A. n.', 'f': None, 'n': 'A.'},
            {'text': 'A. or B. f.', 'f': 'A. or B.', 'n': None},
            {'text': 'A. or B. n.', 'f': None, 'n': 'A. or B.'},
            {'text': '- f.', 'f': None, 'n': None},
            {'text': '- n.', 'f': None, 'n': None},
            {'text': 'A. f. B. n.', 'f': 'A.', 'n': 'B.'},
            {'text': 'A. or C. f. B. n.', 'f': 'A. or C.', 'n': 'B.'},
            {'text': '- f. B. n.', 'f': None, 'n': 'B.'},
            {'text': 'A. or C. f. B. or D. n.', 'f': 'A. or C.',
             'n': 'B. or D.'},
            {'text': 'A. or C. f. - n.', 'f': 'A. or C.', 'n': None},
            {'text': '- f. - n.', 'f': None, 'n': None},
        ]
        self.other_names = [
            {'other_names': 'Name', 'other_names_plain': 'Name'},
            {'other_names': '(Name)', 'other_names_plain': 'Name'},
            {'other_names': '(\'Name\')', 'other_names_plain': 'Name'},
            {'other_names': '(=? I.? Name Surname)',
             'other_names_plain': 'I. Name Surname'},
            {'other_names': '(= Name Surname)',
             'other_names_plain': 'Name Surname'},
            {'other_names': '(12) Name', 'other_names_plain': 'Name'},
        ]
        self.person = Person()

    def test__f(self):
        # 1. fail the test
        # self.fail()
        # 2. easy pass of the test
        # self.assertIsNone(self.person.f)
        # 3. add test cases and iteratively implement the functionality to pass
        for filiation in self.filiations:
            self.person.filiation = filiation['text']
            self.assertEqual(filiation['f'], self.person.f)

    def test__n(self):
        for filiation in self.filiations:
            self.person.filiation = filiation['text']
            self.assertEqual(filiation['n'], self.person.n)

    def test__other_names_plain(self):
        for on in self.other_names:
            self.person.other_names = on['other_names']
            self.assertEqual(on['other_names_plain'],
                             self.person.other_names_plain)
