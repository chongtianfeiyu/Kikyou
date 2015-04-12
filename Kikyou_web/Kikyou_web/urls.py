from django.conf.urls import patterns, include, url 
from django.conf import *
from srvMonitor.views import * 
from verIntegration.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Kikyou_web.views.home', name='home'),
    # url(r'^Kikyou_web/', include('Kikyou_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
	
	url(r'^srvlist/$',srvlist),
	url(r'^tmpstatus/$',tmpstatus),
	url(r'^srvstatus/$',srvstatus),
    
    url(r'^$',index),
    url(r'^index/$',index),
    url(r'^login/$',login),
    url(r'^logout/$',logout),
    
    url(r'^versionstart/$',versionStart),
    url(r'^uiprepare/$',uiprepare),
	url(r'^binprepare/$',binprepare),
    url(r'^uploadcdn/$',uploadcdn),
    url(r'^uploadpng/$',uploadpng),
    url(r'^test/$',test),
)
