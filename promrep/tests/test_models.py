from django.test import TestCase
from promrep.models import (DateInformation, NoteType, Person, PersonNote,
                            PostAssertion, Praenomen, SecondarySource)


class PersonTest(TestCase):

    def setUp(self):
        self.dprr_ids = [
            {'nomen': None, 'id': 1, 'dprr_id': None},
            {'nomen': 'Iulius', 'id': 1957, 'dprr_id': 'IULI1957'},
            {'nomen': 'Tullius', 'id': 72, 'dprr_id': 'TULL0072'},
            {'nomen': 'Yo', 'id': 1, 'dprr_id': 'YO0001'},
        ]
        self.filiations = [
            {'text': None, 'f': None, 'n': None},
            {'text': '', 'f': None, 'n': None},
            {'text': 'ABC', 'f': None, 'n': None},
            {'text': 'T. f.', 'f': ['Titus'], 'n': None},
            {'text': 'A. n.', 'f': None, 'n': ['Aulus']},
            {'text': 'A. or K. f.', 'f': ['Aulus', 'Caeso'], 'n': None},
            {'text': 'A. or K. n.', 'f': None, 'n': ['Aulus', 'Caeso']},
            {'text': '- f.', 'f': None, 'n': None},
            {'text': '- n.', 'f': None, 'n': None},
            {'text': 'A. f. T. n.', 'f': ['Aulus'], 'n': ['Titus']},
            {'text': 'A. or C. ? f. K. n.', 'f': ['Aulus', 'Gaius', 'Caius'],
             'n': ['Caeso']},
            {'text': '- f. K. n.', 'f': None, 'n': ['Caeso']},
            {'text': 'A. or C. f. Cn. or Her. n.',
             'f': ['Aulus', 'Gaius', 'Caius'],
             'n': ['Gnaeus', 'Cnaeus', 'Herius']},
            {'text': 'A. or C. f. - n.', 'f': ['Aulus', 'Gaius', 'Caius'],
             'n': None},
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
        self.praenomens = [
            {'name': 'Aulus', 'abbrev': 'A.'},
            {'name': 'Caeso', 'abbrev': 'K.'},
            {'name': 'Gaius', 'abbrev': 'C.'},
            {'name': 'Gnaeus', 'abbrev': 'Cn.'},
            {'name': 'Herius', 'abbrev': 'Her.'},
            {'name': 'Titus', 'abbrev': 'T.'},
        ]

        self.person = Person()

        for p in self.praenomens:
            Praenomen(name=p['name'], abbrev=p['abbrev']).save()

    def test__dprr_id(self):
        for item in self.dprr_ids:
            self.person.id = item['id']
            self.person.nomen = item['nomen']
            self.assertEqual(item['dprr_id'], self.person.dprr_id)

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


class PraenomenTest(TestCase):

    def setUp(self):
        self.praenomens = [
            {'name': 'Aulus', 'abbrev': 'A.', 'alternate_name': None},
            {'name': 'Caeso', 'abbrev': 'K.', 'alternate_name': None},
            {'name': 'Gaius', 'abbrev': 'C.', 'alternate_name': 'Caius'},
            {'name': 'Gnaeus', 'abbrev': 'Cn.', 'alternate_name': 'Cnaeus'},
            {'name': 'Herius', 'abbrev': 'Her.', 'alternate_name': None},
            {'name': 'Titus', 'abbrev': 'T.', 'alternate_name': None},
        ]

    def test__has_alternate_name(self):
        for p in self.praenomens:
            praenomen = Praenomen(name=p['name'], abbrev=p['abbrev'])
            self.assertEqual(
                p['alternate_name'] is not None,
                praenomen.has_alternate_name())

    def test__alternate_name(self):
        for p in self.praenomens:
            praenomen = Praenomen(name=p['name'], abbrev=p['abbrev'])
            self.assertEqual(
                p['alternate_name'], praenomen.alternate_name)


class DateInformationTest(TestCase):

    def setUp(self):
        self.date_info_empty = DateInformation()

        ss = SecondarySource(name='Broughton', abbrev_name='Broughton')
        self.date_info_broughton = DateInformation(secondary_source=ss)

        ss = SecondarySource(name='Ruepkeeeeeee', abbrev_name='RUEPKE')
        self.date_info_ruepke_upper = DateInformation(secondary_source=ss)

        ss = SecondarySource(name='Ruepkeeeeeee', abbrev_name='ruepke')
        self.date_info_ruepke_lower = DateInformation(secondary_source=ss)

    def test__has_ruepke_secondary_source(self):
        self.assertFalse(self.date_info_empty.has_ruepke_secondary_source())
        self.assertFalse(
            self.date_info_broughton.has_ruepke_secondary_source())
        self.assertTrue(
            self.date_info_ruepke_upper.has_ruepke_secondary_source())
        self.assertTrue(
            self.date_info_ruepke_lower.has_ruepke_secondary_source())


class PostAssertionTest(TestCase):

    def setUp(self):
        self.pa_empty = PostAssertion(secondary_source=SecondarySource())

        person = Person()
        ss = SecondarySource(name='Broughton', abbrev_name='Broughton')
        self.pa_broughton = PostAssertion(secondary_source=ss)
        self.pa_broughton.person = person

        note_ss = SecondarySource(name='x', abbrev_name='y')
        note_ss.save()

        note_type = NoteType(name='x')
        note_type.save()

        note = PersonNote(
            note_type=note_type, secondary_source=note_ss, text='hello')
        note.save()

        person = Person()
        person.save()
        person.notes.add(note)

        ss = SecondarySource(name='Ruepkeeeeeee', abbrev_name='RUEPKE')
        self.pa_ruepke_upper = PostAssertion(secondary_source=ss)
        self.pa_ruepke_upper.person = person

        note_type = NoteType(name='ruepke_B')
        note_type.save()

        self.note_text = 'note text'
        note = PersonNote(note_type=note_type, secondary_source=note_ss,
                          text=self.note_text)
        note.save()

        person = Person()
        person.save()
        person.notes.add(note)

        ss = SecondarySource(name='Ruepkeeeeeee', abbrev_name='ruepke')
        self.pa_ruepke_lower = PostAssertion(secondary_source=ss)
        self.pa_ruepke_lower.person = person

    def test__has_ruepke_secondary_source(self):
        self.assertFalse(self.pa_empty.has_ruepke_secondary_source())
        self.assertFalse(self.pa_broughton.has_ruepke_secondary_source())
        self.assertTrue(self.pa_ruepke_upper.has_ruepke_secondary_source())
        self.assertTrue(self.pa_ruepke_lower.has_ruepke_secondary_source())

    def test__get_ruepke_notes(self):
        self.assertIsNone(self.pa_empty.get_ruepke_notes())
        self.assertIsNone(self.pa_broughton.get_ruepke_notes())
        self.assertEqual('', self.pa_ruepke_upper.get_ruepke_notes())
        self.assertEqual(self.note_text,
                         self.pa_ruepke_lower.get_ruepke_notes())
