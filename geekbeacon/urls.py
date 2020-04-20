from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import include, path, re_path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail_feeds.feeds import BasicFeed
from coderedcms import admin_urls as coderedadmin_urls
from coderedcms import search_urls as coderedsearch_urls
from coderedcms import urls as codered_urls

from search import views as search_views

urlpatterns = [
    # Admin
    path('admin/', include(coderedadmin_urls)),
    # path('django-admin/', admin.site.urls),
    # Documents
    path('docs/', include(wagtaildocs_urls)),


    # Search
    path('search/', include(coderedsearch_urls)),
    # the list:
    re_path(r'', include(codered_urls)),

    # url(r'^documents/', include(wagtaildocs_urls)),


    # path('docs/', include(wagtaildocs_urls)),

    # url(r'^search/$', search_views.search, name='search'),

    url(r'^rss$', BasicFeed(), name='basic_feed'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
