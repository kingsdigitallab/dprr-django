from django.conf.urls import patterns, include, url

import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)


#------------------------------------------------------------------------------
# Django Debug Toolbar URLS
#------------------------------------------------------------------------------

try:
    if settings.DEBUG:
        import debug_toolbar
        urlpatterns += patterns('',
            url(r'^__debug__/', include(debug_toolbar.urls)),
        )

except ImportError:
    pass
