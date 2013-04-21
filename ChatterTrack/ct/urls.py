from django.conf.urls import patterns, include, url
from ct.views import index, twitter_login

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ChatterTrack.views.home', name='home'),
    # url(r'^ChatterTrack/', include('ChatterTrack.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),    
    url(r'^twitter_login/$', twitter_login),
    url(r'^$', index),
)
