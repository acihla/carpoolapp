from django.conf.urls import patterns, include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^rider/', include('carpoolapp.urls')),
    url(r'^driver/', include('carpoolapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
