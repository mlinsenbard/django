from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('homepage.views',
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'home'),
    url(r'^blog/$', 'blog'),
    url(r'^programming/$', 'programming'),
    url(r'^music/$', 'music'),
    #url(r'^about/$', 'about'),
    url(r'^contact/$', 'contact'),
    url(r'^admin/', include(admin.site.urls)),
)
