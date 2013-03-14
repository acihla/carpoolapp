from django.utils import simplejson as json
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import  send_mail,BadHeaderError

from carpoolapp.models import *
from carpoolapp.unitTest import *

from django.core.serializers.json import DjangoJSONEncoder
import os
import json
import sys
import tempfile
import traceback
import re
import StringIO
import unittest
from googlemaps import GoogleMaps

#connecting using api key for alex.cihla@gmail.com
gmaps = GoogleMaps("AIzaSyAGf-Mbj40HtzmRmOvPWZX4RnE2RIG_tzc")

def search(request):
	routes = Route.objects.all()
	resp = {"error":"Success"}
	rides = []
	for route in routes:
		entry = {}
		entry["driver"] = route.driver
		entry["rider"] = route.rider
		entry["depart_time"] = route.depart_time
		#entry["arrival_time"] = route.depart_time
		#entry["depart_lat"] = route.depart_lat
		#entry["depart_lg"] = route.depart_lg
		#entry["arrive_lat"] = route.arrive_lat
		#entry["arrive_lg"] = route.arrive_lg
        entry["maps_info"] = route.maps_info
		entry["status"] = route.status

		rides.append(entry)


	resp["rides"] = rides
	return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

def addroute(request):
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
def select_ride(request):
  
  try:
    data = json.loads(request.raw_post_data)
    rider_id = data['rider_id']
    print rider_id
    route_id = data['route_id']
    print route_id
    rider = User.objects.get(id=rider_id)
    route = Route.objects.get(id=route_id)
    driver_info =route.driver
    driver_email = driver_info.driver.email
    print driver_email
    route.rider = rider
    route.save()
  except KeyError:
    return HttpResponse(simplejson.dumps({'errCode':-1}),content_type="application/json")
  try:
    send_mail('email from my app','so it is working','carpoolcs169@gmail.com',[driver_email],fail_silently=False,auth_user=None ,auth_password=None, connection=None)
  except BadHeaderError:
    return HttpResponse('bad header found')

  return HttpResponse(simplejson.dumps({'errCode':1}),content_type="application/json")



def TESTAPI_resetFixture(request):
    #need to clear db here !!!
    resp = {"errCode" : SUCCESS}
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")


def TESTAPI_unitTests(request):
    buffer = StringIO.StringIO()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTest)
    result = unittest.TextTestRunner(stream = buffer, verbosity = 2).run(suite)

    rv = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": buffer.getvalue()}
    return HttpResponse(json.dumps(rv), content_type = "application/json")