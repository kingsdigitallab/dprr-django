import unittest

from django.test import TestCase
from promrep.forms import PromrepFacetedSearchForm


@unittest.skip("Skipping for now...")
class PromrepFacetedSearchFormTest(TestCase):
    def setUp(self):
        self.form = PromrepFacetedSearchForm()

    def test_no_query_found(self):
        self.assertIsNotNone(self.form.no_query_found())

    def test_empty_search(self):
        # cannot compare objects
        # naively comparing first element and count of elements

        expected = self.form.no_query_found()
        result = self.form.search()

        self.assertEqual(expected.count(), result.count())
        self.assertEqual(expected[0].id, result[0].id)
