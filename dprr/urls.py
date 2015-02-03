from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

# from wagtail.wagtailcore import urls as wagtail_urls
# from wagtail.wagtailadmin import urls as wagtailadmin_urls
# from wagtail.wagtaildocs import urls as wagtaildocs_urls
# from wagtail.wagtailsearch.urls import frontend as wagtailsearch_frontend_urls

# Signal handlers
# from wagtail.wagtailsearch.signal_handlers import register_signal_handlers as \
#     wagtailsearch_register_signal_handlers
# wagtailsearch_register_signal_handlers()
#
# from ddhldap.signal_handlers import register_signal_handlers as \
#     ddhldap_register_signal_handlers

# ddhldap_register_signal_handlers()

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    )

try:
    if settings.DEBUG:
        import debug_toolbar
        urlpatterns += patterns('',
            url(r'^__debug__/', include(debug_toolbar.urls)),
        )

except ImportError:
    pass

# urlpatterns += patterns('',
#                         url(r'^wagtail/images/', include(wagtailimages_urls)),
#                         url(r'^wagtail/embeds/', include(wagtailembeds_urls)),
#                         url(r'^wagtail/documents/',
#                             include(wagtaildocs_admin_urls)),
#                         url(r'^wagtail/snippets/',
#                             include(wagtailsnippets_urls)),
#                         url(r'^wagtail/search/',
#                             include(wagtailsearch_admin_urls)),
#                         url(r'^wagtail/users/', include(wagtailusers_urls)),
#                         url(r'^wagtail/redirects/',
#                             include(wagtailredirects_urls)),
#                         url(r'^wagtail/', include(wagtailadmin_urls)),
#                         url(r'^search/', include(wagtailsearch_frontend_urls)),
#                         url(r'^documents/', include(wagtaildocs_urls)),
#
#                         url(r'', include(wagtail_urls)),
#                         )

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import os.path

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(settings.MEDIA_ROOT,
                                                     'images'))
