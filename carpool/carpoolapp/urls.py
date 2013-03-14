from django.conf.urls import patterns, include, url

urlpatterns = patterns('carpoolapp.views',
    url(r'^search', 'search'),
    url(r'^addroute', 'addroute'),
    url(r'^select','select_ride'),
    url(r'^resetFixture', 'TESTAPI_resetFixture'),
    url(r'^unitTests', 'TESTAPI_unitTests'),
)