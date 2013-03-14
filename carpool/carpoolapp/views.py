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

#responses to be handled by application
SUCCESS               =   1  # : a success
ERR_BAD_DEPARTURE  =  -1  # : Departure location is not valid
ERR_BAD_DESTINATION       =  -2  # : Destination location is not valid
ERR_BAD_USERID      =  -3  # : UID does not exist in db, or is not a driver
ERR_BAD_TIME     =  -4   #format for time is bad
MAX_LENGTH_IN = 200  #max length for all datums in our db



def search(request):
    resp = {"error":"Success"}
    try:
        routes = Route.objects.all()
        resp["size"] = len(routes)
        rides = []
        for route in routes:
            entry = {}
            driverinfo = models.instance_dict(route.driver)
            driverinfo["driver"] = models.instance_dict(route.driver.driver)
            entry["driver"] = driverinfo
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
    except:
            resp["error"] = "ERROR"
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

def addroute(request):
    rdata = json.loads(request.body)
    uid = rdata.get("user", "")
    start = rdata.get("start", "")
    end = rdata.get("end", "")
    departTime = rdata.get("edt", "")
    validDatums = handleRouteData(uid, start, end, depart)
    if (validDatums != 1):
    	resp = {"errCode" : validDatums}
    else:
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
                directions=[]
                count = 0
                #for adding turn by turn directions later
                for step in trip['steps']:
                    indstep = step['html_instructions']
                    indstep = indstep.replace('</b>', '')
                    indstep = indstep.replace('<b>', '')
                    indstep = indstep.replace('/<wbr/>', '')
                    indstep = indstep.replace('<div style="font-size:0.9em">', ' *** ')
                    indstep = indstep.replace('<div class="">', ' *** ')
                    indstep = indstep.replace('<div class="google_note">', ' *** ')
                    indstep = indstep.replace('</div>', ' *** ')
                    directions[count] = indstep
                    count += 1

            
            newRoute = Route(driver = uid, rider = "", depart_time = depart, maps_info = currentRoute, status = 0)
            newRoute.save()

            resp = {"errCode" : 1}

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


def handleRouteData(uid, start, end, depart):
	if(start.length > MAX_LENGTH_IN):
		return ERR_BAD_DEPARTURE
	if(end.length > MAX_LENGTH_IN):
		return ERR_BAD_DESTINATION
	if(DriverInfo.objects.get(driver = uid)):
		return ERR_BAD_USERID
	return SUCCESS


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