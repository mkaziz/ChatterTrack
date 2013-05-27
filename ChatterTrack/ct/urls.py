from django.conf.urls import patterns, include, url
from ct.views import index, twitter_login, login, twitter_authenticated, dashboard, datasiftLog, datasiftStop, datasiftPushLog, analyzeStream, getStreamedTweets, deleteStream, stopStream

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
    url(r'^twitter_authenticated/$', twitter_authenticated),
    url(r'^login/$', login), 
    url(r'^dashboard/$', dashboard),
    url(r'^stopStream/$', stopStream),
    url(r'^deleteStream/$', deleteStream),
    url(r'^analyzeStream/$', analyzeStream),
    url(r'^getStreamedTweets/$', getStreamedTweets),
    url(r'^datasiftLog/$', datasiftLog),
    url(r'^datasiftPushLog/$', datasiftPushLog),
    url(r'^datasiftStop/$', datasiftStop),
    url(r'^$', index),
)
