from django.conf.urls import patterns, include, url
from django.contrib.gis import admin
from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
                       ('^admin/', include(admin.site.urls)),
                       )

# Filebrowser admin media library.
if getattr(settings, 'PACKAGE_NAME_FILEBROWSER') in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                            ('^admin/media-library/',
                             include('%s.urls' %
                                     settings.PACKAGE_NAME_FILEBROWSER)),
                            )

urlpatterns += patterns('',
                        # homepage as static template
                        url('^$', direct_to_template,
                            {'template': 'index.html'}, name='home'),

                        url('^', include('mezzanine.urls')),
                        )

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = 'mezzanine.core.views.page_not_found'
handler500 = 'mezzanine.core.views.server_error'
