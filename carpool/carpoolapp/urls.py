from django.conf.urls import patterns, include, url

urlpatterns = patterns('carpoolapp.views',
    url(r'^search', 'search'),
    url(r'^addroute', 'addroute'),
    url(r'^select','select_ride'),
    url(r'^accept$','accept_ride'),
    url(r'^signup','signup'),
    url(r'^login','login'),
    url(r'^filter','filter'),
    url(r'^feedback','leave_feedback'),
    url(r'^rides_accepted','rides_accepted'),
    url(r'^rides_denied','rides_denied'),
    url(r'^rides_pending','rides_pending'),
    url(r'^rides_canceled','rides_canceled'),
    url(r'^cancel_ride','cancel_ride'),
    url(r'^resetFixture', 'TESTAPI_resetFixture'),
    url(r'^unitTests', 'TESTAPI_unitTests'),
    url(r'^delete_route', 'delete_route'),
    url(r'^deleterides', 'deleteRides'),
    url(r'^generateexamples', 'generateExamples'),
    url(r'^getProfile', 'getProfile'),
    url(r'^changePassword', 'changePassword'),
    url(r'^changeUserInfo', 'changeUserInfo'),
    url(r'^changeDriverInfo', 'changeDriverInfo'),
    url(r'^manageRoute', 'manageRoute'),
    url(r'^manageRequest', 'manageRequest')
    url(r'^managePendingRequest', 'managePendingRequest')
    url(r'^manageAcceptedRequest', 'manageAcceptedRequest')
)
