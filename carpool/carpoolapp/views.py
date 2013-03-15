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
from datetime import *

#connecting using api key for alex.cihla@gmail.com
gmaps = GoogleMaps("AIzaSyAGf-Mbj40HtzmRmOvPWZX4RnE2RIG_tzc")

#responses to be handled by application
SUCCESS               =   1  # : a success
ERR_BAD_DEPARTURE  =  -1  # : Departure location is not valid
ERR_BAD_DESTINATION       =  -2  # : Destination location is not valid
ERR_BAD_USERID      =  -3  # : UID does not exist in db, or is not a driver
ERR_BAD_TIME     =  -4   #format for time is bad
ERR_DATABASE_SEARCH_ERROR   = -5  
ERR_BAD_HEADER= -6
ERR_BAD_SERVER_RESPONSE = -7
MAX_LENGTH_IN = 200  #max length for all datums in our db

sample_date = date(1992,4,17)
@csrf_exempt
def search(request):
    try:
        rdata = json.loads(request.body)
    except Exception, err:
        print str(err)
    #TODO Parse json here.
    resp = {"errCode":SUCCESS}
    try:
        routes = Route.objects.all()
        rides = []
        for route in routes:
            #TODO filter routes to fit request.
            entry = route.to_dict()
            if entry.get("status", "True") == "False":
                rides.append(entry)

        resp["rides"] = rides
        resp["size"] = len(rides)
        #return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    except Exception, err:
            resp["errCode"] = ERR_DATABASE_SEARCH_ERROR
            resp["errMsg"] = str(err)
            print str(err)
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

@csrf_exempt
def addroute(request):
    rdata = json.loads(request.body)
    uid = rdata.get("user", "")
    #start = rdata.get("start", "")
    #end = rdata.get("end", "")

    departLocLong = rdata.get("depart-long", "")
    departLocLat = rdata.get("depart-lat", "")

    destinationLocLong = rdata.get("dest-long", "")
    destinationLocLat = rdata.get("dest-lat", "")

    departTime = sample_date #rdata.get("edt", "")
    validDatums = 1; #handleRouteData(uid, start, end, depart)
    if (validDatums != 1):
    	resp = {"errCode" : validDatums}

    else:
        newRoute = Route(driver_info = DriverInfo.objects.get(id = 1), rider = None, depart_lat = departLocLat, depart_lg = departLocLong, arrive_lat = destinationLocLat, arrive_lg = destinationLocLong, depart_time = departTime, status = False) #maps_info = directions, 
        newRoute.save()

        resp = {"errCode" : SUCCESS}
        """
        try:

            
            currentRoute = gmaps.directions(start, end)
            directions= ""
            route = currentRoute['routes'][0]
            legs = route['legs']

            #dealing with possible multiple legs due to utilization of a waypoint
            for trip in legs:
                #print primRoute['routes'][end_location]
                #printing time and distance of route
                routeTime = trip['duration']['value'] / 60
                routeDist = trip['distance']['value'] * 0.000621371
                #formatting and printing each step
                
                
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
                    directions += indstep 
                    
            

            
            

        except Exception, err:
            resp = {"errCode" : err}
    """
    
    
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
        driver_info =route.driver_info
        driver_email = driver_info.driver.email
        print driver_email
        route.rider = rider
        route.save()
        url = "http://127.0.0.1:8000/driver/accept"
        url += "?route_id=" + str(route_id)
        yesUrl = url + "&response=1"
        noUrl = url + "&response=0"
        message = rider.firstname +" "+rider.lastname+ "would like a ride from you to accept, please click on the following link \n" + yesUrl + "\n to deny click, \n" + noUrl


    except KeyError:
        return HttpResponse(json.dumps({'errCode':ERR_DATABASE_SEARCH_ERROR}),content_type="application/json")

    except Exception, err:
        return HttpResponse(json.dumps({'errCode':ERR_DATABASE_SEARCH_ERROR}),content_type="application/json")
    try:
        send_mail('Carpool Ride Notification',message,'carpoolcs169@gmail.com',[driver_email],fail_silently=False,auth_user=None ,auth_password=None, connection=None)
    except BadHeaderError:
        return HttpResponse(json.dumps({'errCode':ERR_BAD_HEADER}),content_type="application/json")

    return HttpResponse(json.dumps({'errCode':SUCCESS}),content_type="application/json")

@csrf_exempt
def accept_ride(request):
  print 'in accept ride'
  try:
    r = json.loads(request.body)
    route_id = r.get("route_id", -1)
    response = r.get("response", "") #-1) What is going on here? this is request right? Why do we have a response segment?
    print "route id: " + str(route_id)
    print "response: " + str(response)
    route = Route.objects.get(id=route_id)
    """if response == "1":
        route.status='True'
        route.save()
    elif response == "0":
        route.status = 'False'
        route.save()
    else:
        raise Exception("Invalid response" + str(response))
    """
  except Exception, err:
    print str(err)
    return HttpResponse(json.dumps({'errCode':ERR_BAD_SERVER_RESPONSE}),content_type="application/json")

  return HttpResponse(json.dumps({'errCode':SUCCESS}),content_type="application/json")


def handleRouteData(uid, start, end, depart):
	if(len(start) > MAX_LENGTH_IN):
		return ERR_BAD_DEPARTURE #-1
	if(len(end) > MAX_LENGTH_IN):
		return ERR_BAD_DESTINATION #-2
	if not (DriverInfo.objects.get(id = uid)):
		return ERR_BAD_USERID #-3
	return SUCCESS #1

@csrf_exempt
def TESTAPI_resetFixture(request):
    #need to clear db here !!! Not necessary if running python manage.py test carpoolapp
    resp = {"errCode" : SUCCESS}
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

@csrf_exempt
def TESTAPI_unitTests(request):
    buffer = StringIO.StringIO()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTest)
    result = unittest.TextTestRunner(stream = buffer, verbosity = 2).run(suite)

    rv = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": buffer.getvalue()}
    return HttpResponse(json.dumps(rv), content_type = "application/json")
