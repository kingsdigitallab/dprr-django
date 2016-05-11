from django.test import TestCase
from wagtailbase.models import (
    IndexPage,
    RichTextPage,
    BlogIndexPage,
    BlogPost,
    IndexPageRelatedLink)

from wagtail.wagtailcore.models import Page


FIXTURES = ['test_data.json']


class TestRelatedLink(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.link = IndexPageRelatedLink.objects.get(id=1)

    def test_link(self):
        self.assertEqual('http://www.duckduckgo.com/', self.link.link)


class TestIndexPage(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.index_page = IndexPage.objects.filter(
            slug='standard-index').first()
        self.child_page = RichTextPage.objects.filter(
            slug="first-page-index").first()

    def test_children(self):
        self.assertEqual(2, len(self.index_page.children))

        self.assertEqual(self.child_page,
                         self.index_page.get_children().first().specific)
        self.assertEqual(self.child_page, self.index_page.children.first().specific)


class TestRichTextPage(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.index_page = IndexPage.objects.filter(
            slug='standard-index').first()
        self.page = RichTextPage.objects.filter(
            slug="first-page-index").first()

    def test_index_page(self):
        self.assertEqual(self.index_page, self.page.index_page.specific)


class TestBlogIndexPage(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.blog = BlogIndexPage.objects.filter(slug='blog').first()
        self.post = BlogPost.objects.filter(slug="s-it").first()

    def test_posts(self):
        self.assertEqual(self.post, self.blog.posts.last().specific)
