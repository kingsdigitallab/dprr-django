import logging

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
from django.template.loader import select_template
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

logger = logging.getLogger(__name__)


class AbstractLinkField(models.Model):

    """Abstract class for link fields."""

    link_document = models.ForeignKey(
        "wagtaildocs.Document",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    link_external = models.URLField("External link", blank=True, null=True)
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    panels = [
        DocumentChooserPanel("link_document"),
        FieldPanel("link_external"),
        PageChooserPanel("link_page"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    class Meta:
        abstract = True


class AbstractRelatedLink(AbstractLinkField):

    """Abstract class for related links."""

    title = models.CharField(max_length=256, help_text="Link title")

    panels = [FieldPanel("title"), MultiFieldPanel(AbstractLinkField.panels, "Link")]

    class Meta:
        abstract = True


class AbstractAttachment(AbstractLinkField):
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel("image"),
        FieldPanel("embed_url"),
        FieldPanel("caption"),
        MultiFieldPanel(AbstractLinkField.panels, "Link"),
    ]

    class Meta:
        abstract = True


class BasePage(Page):

    """Abstract class Page. This class is not abstract to Django because
    it needs access to the manager. It will not appear in the Wagtail
    admin, however.

    It implements methods to overload routing and serving multiple views
    on a page. Based in the SuperPage class from wagtail here:
    https://gist.github.com/kaedroho/10296244#file-superpage-py

    All pages in wagtailbase inherit from this class."""

    is_creatable = False

    @classmethod
    def register_subpage_type(cls, new_page_type):
        """Registers a new kind of subpage that this page can be a parent """
        cls.subpage_types = cls.subpage_types + [new_page_type]

    def is_current_or_ancestor(self, page):
        """Returns True if the given page is the current page or is an ancestor
        of the current page."""
        page = page.specific

        if self.id == page.id:
            return True

        parent = self.get_parent().specific

        if (
            parent
            and isinstance(parent, BasePage)
            and parent.is_current_or_ancestor(page)
        ):
            return True

        return False

    def get_template(self, request, *args, **kwargs):
        """Checks if there is a template with the page path, and uses that
        instead of using the generic page type template."""
        page_template = "{0}.html".format(self.url.strip("/"))
        logger.debug("get_template: page_template: {0}".format(page_template))
        default_template = super(BasePage, self).get_template(request, *args, **kwargs)
        logger.debug("get_template: default_template:{0}".format(default_template))

        template = select_template([page_template, default_template])

        logger.debug("get_template: {0}".format(template.template.name))
        return template.template.name


class BaseIndexPage(RoutablePageMixin, BasePage):

    """Base class for index pages. Index pages are pages that will have
    children pages."""

    introduction = RichTextField(blank=True)

    search_fields = Page.search_fields + [index.SearchField("introduction")]

    is_creatable = False

    @property
    def children(self):
        """Returns a list of the pages that are children of this page."""
        return self.get_children().filter(live=True)

    @route(r"^$")
    def serve_listing(self, request):
        """Renders the children pages."""
        pages = self.children

        # Pagination
        page = request.GET.get("page")
        paginator = Paginator(pages, settings.ITEMS_PER_PAGE)

        try:
            pages = paginator.page(page)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            pages = paginator.page(1)

        return render(
            request, self.get_template(request), {"self": self, "pages": pages}
        )


class BaseRichTextPage(BasePage):

    """Base class for rich text pages."""

    content = RichTextField()

    search_fields = Page.search_fields + [index.SearchField("content")]

    is_creatable = False

    @property
    def index_page(self):
        """Finds and returns the index page from the page ancestors. If no
        index page is found in the ancestors, it returns the first page."""
        for ancestor in reversed(self.get_ancestors()):
            if isinstance(ancestor.specific, BaseIndexPage):
                return ancestor

        # No ancestors are index pages, returns the first page
        return Page.objects.first()
