from django.conf.urls import patterns, include, url

urlpatterns = patterns('carpoolapp.views',
    url(r'^search', 'search'),
    url(r'^addroute', 'addroute'),
    url(r'^select','select_ride'),
    url(r'^accept','accept_ride'),
    url(r'^signup','signup'),
    url(r'^login','login'),
    url(r'^filter','filter'),
    url(r'^resetFixture', 'TESTAPI_resetFixture'),
    url(r'^unitTests', 'TESTAPI_unitTests'),
    url(r'^deleterides', 'deleteRides'),
    url(r'^generateexamples', 'generateExamples'),
    url(r'^getProfile', 'getProfile'),
)
