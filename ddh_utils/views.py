import haystack.views
import utils


class BaseSearchView (object):

    def build_page(self):
        paginator, page = utils.create_pagination(
            self.results, self.results_per_page, self.request.GET.get('page'))
        return paginator, page

    def _extra_context(self):
        # Add the QueryDict of the request's GET parameters, as needed
        # for pagination and facet display.
        extra = {'querydict': self.request.GET}
        return extra


class SearchView (BaseSearchView, haystack.views.SearchView):

    def extra_context(self):
        extra = super(SearchView, self).extra_context()
        extra.update(super(SearchView, self)._extra_context())
        return extra


class FacetedSearchView (BaseSearchView, haystack.views.FacetedSearchView):

    def extra_context(self):
        extra = super(FacetedSearchView, self).extra_context()
        extra.update(super(FacetedSearchView, self)._extra_context())
        return extra
