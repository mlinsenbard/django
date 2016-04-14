from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('homepage.views',
    url(r'^$', 'home'),
    url(r'^blog/$', 'blog'),
    url(r'^projects/$', 'projects'),
    url(r'^music/$', 'music'),
    url(r'^contact/$', 'contact'),
    url(r'^lol/$', 'lol'),
    url(r'^mxpo/$', 'mxpo'),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
