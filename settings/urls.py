from django.conf.urls import patterns, include, url
from django.contrib import admin
address = ''
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^init/','portal.views.initUser'),
    url(r'^login/','portal.views.login'),
    url(r'^upload/','portal.views.uploadFile'),
    url(r'^like1/','portal.views.like1'),
    url(r'^like2/','portal.views.like2'),
    url(r'^rank1/','portal.views.rank1'),
    url(r'^rank2/','portal.views.rank2'),
    url(r'^info/','portal.views.info'),
    url(r'^startupload/','portal.views.startUpload'),
    url(r'^endupload/','portal.views.endUpload'),
    url(r'^startticket/','portal.views.startTickets'),
    url(r'^startticket1/','portal.views.startTickets1'),
    url(r'^startticket2/','portal.views.startTickets2'),
    url(r'^endticket/','portal.views.endTickets'),
    url(r'^backendlogin/','portal.views.backendLogin'),
    url(r'^alreadylogin/','portal.views.alreadyLogin'),
)
