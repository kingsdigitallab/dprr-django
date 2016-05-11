from base import (AbstractRelatedLink, AbstractAttachment,
                  BaseIndexPage, BaseRichTextPage)

from datetime import date

from django.db import models
from django.conf import settings
from django.conf.urls import url
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render

from taggit.models import TaggedItemBase

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel)
from wagtail.wagtailcore.models import Orderable
from wagtail.contrib.wagtailroutablepage.models import route
from wagtailbase.util import unslugify

from wagtail.wagtailsearch import index

import calendar
import logging

logger = logging.getLogger(__name__)


class IndexPage(BaseIndexPage):
    search_name = 'Index Page'
    subpage_types = ['IndexPage', 'RichTextPage', 'BlogIndexPage']


class IndexPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('wagtailbase.IndexPage',
                       related_name='related_links')


class IndexPageAttachment(Orderable, AbstractAttachment):
    page = ParentalKey('wagtailbase.IndexPage',
                       related_name='attachments')

IndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('introduction', classname='full'),
    InlinePanel(IndexPage, 'related_links', label='Related links'),
    InlinePanel(IndexPage, 'attachments', label='Attachments')
]

IndexPage.promote_panels = [
    MultiFieldPanel(BaseIndexPage.promote_panels, "Common page configuration"),
]


class RichTextPage(BaseRichTextPage):
    search_name = 'Rich Text Page'
    subpage_types = []


class RichTextPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('wagtailbase.RichTextPage',
                       related_name='related_links')


class RichTextAttachment(Orderable, AbstractAttachment):
    page = ParentalKey('wagtailbase.RichTextPage',
                       related_name='attachments')


RichTextPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('content', classname='full'),
    InlinePanel(RichTextPage, 'related_links', label='Related links'),
    InlinePanel(RichTextPage, 'attachments', label='Attachments')
]

RichTextPage.promote_panels = [
    MultiFieldPanel(BaseRichTextPage.promote_panels,
                    "Common page configuration"),
]


class HomePage(BaseRichTextPage):
    search_name = 'Home Page'
    subpage_types = ['IndexPage', 'RichTextPage', 'BlogIndexPage']

    class Meta:
        verbose_name = 'Homepage'


class HomePageAttachment(Orderable, AbstractAttachment):
    page = ParentalKey('wagtailbase.HomePage',
                       related_name='attachments')


HomePage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('content', classname='full'),
    InlinePanel(HomePage, 'attachments', label='Attachments')
]

HomePage.promote_panels = [
    MultiFieldPanel(BaseRichTextPage.promote_panels,
                    "Common page configuration"),
]


class BlogIndexPage(BaseIndexPage):
    search_name = 'Blog'

    subpage_types = ['BlogPost']

    @property
    def posts(self):
        """Returns a list of the blog posts that are children of this page."""
        return BlogPost.objects.filter(
            live=True, path__startswith=self.path).order_by('-date')

    @property
    def active_months(self):
        dates = self.posts.values('date').distinct()
        new_dates = set([date(d['date'].year, d['date'].month, 1)
                         for d in dates])

        return sorted(new_dates, reverse=True)

    def _paginate(self, request, posts):
        """ Paginate posts """

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(posts, settings.ITEMS_PER_PAGE)

        try:
            posts = paginator.page(page)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            posts = paginator.page(1)

        return posts

    @route(r'^$')
    def serve_listing(self, request):
        """main listing"""
        posts = self.posts

        return render(request,
                      self.get_template(request),
                      {'self': self,
                       'posts': self._paginate(request, posts)})

    @route(r'^author/(?P<author>[\w ]+)/$')
    def author(self, request, author=None):
        """listing of posts by a specific author"""

        if not author:
            # Invalid author filter
            raise Http404('Invalid Author')

        posts = self.posts.filter(
            models.Q(owner__username=author) |
            models.Q(owner__username=unslugify(author)))

        return render(request,
                      self.get_template(request),
                      {'self': self,
                       'posts': self._paginate(request, posts),
                       'filter_type': 'author',
                       'filter': author})

    @route(r'^tag/(?P<tag>[\w ]+)/$')
    def tag(self, request, tag=None):
        """listing of posts in a specific tag"""
        if not tag:
            # Invalid tag filter
            raise Http404('Invalid Tag')

        posts = self.posts.filter(
            models.Q(tags__name=tag) |
            models.Q(tags__name=unslugify(tag)))

        return render(request,
                      self.get_template(request),
                      {'self': self,
                       'posts': self._paginate(request, posts),
                       'filter_type': 'tag',
                       'filter': tag})

    @route((r'^date'
            r'/(?P<year>\d{4})'
            r'/$'))
    @route((r'^date'
            r'/(?P<year>\d{4})'
            r'/(?P<month>(?:\w+|\d{1,2}))'
            r'/$'))
    @route((r'^date'
            r'/(?P<year>\d{4})'
            r'/(?P<month>(?:\w+|\d{1,2}))'
            r'/(?P<day>\d{1,2})'
            r'/$'))
    def date(self, request, year=None, month=None, day=None):
        """listing of posts published within a specific year, month, or date"""

        if not year:
            # Invalid year filter
            raise Http404('Invalid Year')

        # filter by date
        date_filter = {'date__year': int(year)}
        date_factory = [int(year)]
        date_format = 'Y'

        if month:
            # specifiec month
            m = self.get_month_number(month.title())

            if m:
                date_filter['date__month'] = m
                date_factory.append(int(m))
            else:
                date_filter['date__month'] = month
                date_factory.append(int(month))

            date_format = 'N Y'
        else:
            # no month defined
            date_factory.append(1)

        if day:
            # specific day defined
            date_filter['date__day'] = int(day)
            date_factory.append(int(day))
            date_format = 'N d, Y'
        else:
            # no day defined
            date_factory.append(1)

        try:
            posts = self.posts.filter(**date_filter)
        except ValueError:
            # Invalid date filter
            raise Http404

        return render(request,
                      self.get_template(request),
                      {'self': self,
                       'posts': self._paginate(request, posts),
                       'filter_type': 'date',
                       'filter_format': date_format,
                       'filter': date(*date_factory)})

    def get_month_number(self, month):
        names = dict((v, k) for k, v in enumerate(calendar.month_name))
        abbrs = dict((v, k) for k, v in enumerate(calendar.month_abbr))

        month_str = month.title()

        try:
            return names[month_str]
        except KeyError:
            try:
                return abbrs[month_str]
            except KeyError:
                return 0


class BlogIndexPageRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('wagtailbase.BlogIndexPage',
                       related_name='related_links')


class BlogIndexPageAttachment(Orderable, AbstractAttachment):
    page = ParentalKey('wagtailbase.BlogIndexPage',
                       related_name='attachments')


BlogIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('introduction', classname='full'),
    InlinePanel(BlogIndexPage, 'related_links', label='Related links'),
    InlinePanel(BlogIndexPage, 'attachments', label='Attachments')
]

BlogIndexPage.promote_panels = [
    MultiFieldPanel(BaseIndexPage.promote_panels,
                    "Common page configuration"),
]


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('wagtailbase.BlogPost',
                                 related_name='tagged_items')


class BlogPost(BaseRichTextPage):
    date = models.DateField('Post Date', default=date.today)
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    featured = models.BooleanField(
        default=False, help_text="Feature this post")

    subpage_types = []

    search_name = 'Blog post'

    search_fields = BaseRichTextPage.search_fields + (
        index.FilterField('date'),
        index.FilterField('featured'),
    )

    @property
    def blog_index(self):
        # Find blog index in ancestors
        for ancestor in reversed(self.get_ancestors()):
            if isinstance(ancestor.specific, BlogIndexPage):
                return ancestor

        # No ancestors are blog indexes,
        # just return first blog index in database
        return BlogIndexPage.objects.first()


class BlogPostRelatedLink(Orderable, AbstractRelatedLink):
    page = ParentalKey('wagtailbase.BlogPost', related_name='related_links')


class BlogPostAttachment(Orderable, AbstractAttachment):
    page = ParentalKey('wagtailbase.BlogPost',
                       related_name='attachments')


BlogPost.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('date'),
    FieldPanel('content', classname='full'),
    InlinePanel(BlogPost, 'related_links', label='Related links'),
    InlinePanel(BlogPost, 'attachments', label='Attachments')
]

BlogPost.promote_panels = [
    FieldPanel('tags'),
    FieldPanel('featured'),
    MultiFieldPanel(BaseRichTextPage.promote_panels,
                    "Common page configuration"),
]
