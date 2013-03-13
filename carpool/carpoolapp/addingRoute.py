from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
import os
import json
import sys
import tempfile
import traceback
import re
import StringIO
import unittest
from polls.unitTest import UnitTest
from googlemaps import GoogleMaps

#connecting using api key for alex.cihla@gmail.com
gmaps = GoogleMaps("AIzaSyAGf-Mbj40HtzmRmOvPWZX4RnE2RIG_tzc")

SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

MAX_USERNAME_LENGTH = 128
MAX_PASSWORD_LENGTH = 128


@csrf_exempt
def setRoute(request):
    rdata = json.loads(request.body)
    username = rdata.get("user", "")
    start = rdata.get("start", "")
    end = rdata.get("end", "")
    depart = rdata.get("edt", "")
    try:
        currentRoute = gmaps.directions(start, end)
        route = currentRoute['routes'][0]
        legs = route['legs']

        #dealing with possible multiple legs due to utilization of a waypoint
        for trip in legs:
            #print primRoute['routes'][end_location]
            #printing time and distance of route
            routeTime = trip['duration']['value'] / 60
            routeDist = trip['distance']['value'] * 0.000621371
            #formatting and printing each step

            """for step in trip['steps']:
                indstep = step['html_instructions']
                indstep = indstep.replace('</b>', '')
                indstep = indstep.replace('<b>', '')
                indstep = indstep.replace('/<wbr/>', '')
                indstep = indstep.replace('<div style="font-size:0.9em">', ' *** ')
                indstep = indstep.replace('<div class="">', ' *** ')
                indstep = indstep.replace('<div class="google_note">', ' *** ')
                indstep = indstep.replace('</div>', ' *** ')
                print indstep"""

        
        newRoute = Route(driver = username, rider = "", depart_time = depart, maps_info = currentRoute, status = 0)
        newRoute.save()

        resp = {"errCode" : SUCCESS}

    except Exception, err:
        resp = {"errCode" : err}
    
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")


@csrf_exempt
def TESTAPI_resetFixture(request):
    #need to clear db here !!!
    resp = {"errCode" : SUCCESS}
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

@csrf_exempt
def TESTAPI_unitTests(request):
    buffer = StringIO.StringIO()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTest)
    result = unittest.TextTestRunner(stream = buffer, verbosity = 2).run(suite)

    rv = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": buffer.getvalue()}
    return HttpResponse(json.dumps(rv), content_type = "application/json")