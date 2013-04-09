from django.utils import simplejson as json
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import  send_mail,BadHeaderError
#from validate_email import validate_email

from carpoolapp.models import *
from carpoolapp.unitTest import *
import testUtils

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
import math

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
MAX_LENGTH_FIRST_LAST_PASS = 20 #max length for first and last name and password
MAX_LENGTH_EMAIL = 50  #max length email
COORD_LENGTH_IN = 15 # max length of coordinates
ERR_BAD_KEY = -8
ERR_NOT_USER = -9
ERR_BAD_EMAIL = -10
ERR_BAD_INPUT_OR_LENGTH = -11
ERR_BAD_DOB = -12
ERR_BAD_JSON = -13
ERR_USER_EXISTS =-14
#sample_date = "1992-04-17"

sex_list = ['male','female']

@csrf_exempt
def signup(request):
    try:
        rdata = json.loads(request.body)
        #import pdb;pdb.set_trace()
        resp = sanitizeSignupData(rdata)
        if resp["errCode"] == SUCCESS:
            firstname = rdata.get("firstname", "")
            lastname = rdata.get("lastname", "")
            email = rdata.get("email", None)
            dob = rdata.get("dob", "")
            sex = rdata.get("sex", "")
            password = rdata.get("password", "")
            cellphone = rdata.get("cellphone", "")
            driver = rdata.get("driver", False)

            date_obj = datetime.strptime("".join(dob.split("-")),'%m%d%Y').date()

            newUser = User(firstname = firstname, lastname = lastname, email = email, dob = date_obj, sex = sex, password = password, cellphone = cellphone, driver = driver)
            newUser.save()
            if (driver):
              resp1 = driver_check(rdata)
              if resp1["errCode"]== SUCCESS:
                license_no = rdata.get("license_no", "")
                license_exp = rdata.get("license_exp", "")
                car_make = rdata.get("car_make", "")
                car_type = rdata.get("car_type", "")
                car_mileage = rdata.get("car_mileage", "")
                max_passengers = rdata.get("max_passengers", "")
                license_date_obj = datetime.strptime("".join(license_exp.split("-")),'%m%d%Y').date()

                newDriverInfo = DriverInfo(driver = User.objects.get(email = email), license_no = license_no, license_exp = license_date_obj, car_make = car_make, car_type = car_type, car_mileage = car_mileage, max_passengers = max_passengers)
                newDriverInfo.save()
              else:
                return HttpResponse(json.dumps(resp1, cls=DjangoJSONEncoder), content_type = "application/json")
        else:
          return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    except Exception, err:
        print str(err)

    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

def  sanitizeSignupData(rdata): 
    firstname = rdata.get("firstname", "")
    lastname = rdata.get("lastname", "")
    email = rdata.get("email", None)
    dob = rdata.get("dob", "")
    sex = rdata.get("sex", "")
    password = rdata.get("password", "")
    cellphone = rdata.get("cellphone", "")
    driver = rdata.get("driver", False)
    resp = {"errCode":SUCCESS}
    try:
      u = User.objects.get(email =email)
      resp["errCode"] = ERR_USER_EXISTS
    except User.DoesNotExist:
      #validate not null and not too long firstname
      if(not firstname or len(firstname)> MAX_LENGTH_FIRST_LAST_PASS):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
      #validate not null and not too long lastname
      if(not lastname or len(lastname)> MAX_LENGTH_FIRST_LAST_PASS):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
      #validate good email
      #if not (email or validate_email(email)):
      #if not (email):
      #resp["errCode"] = ERR_BAD_EMAIL

      emailPattern = re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[       a-zA-Z]{2,6}$", email) 

      if (emailPattern == None ):
        resp["errCode"] = ERR_BAD_EMAIL

      #validate gooe date of birth
      #dob format mm-dd-yyyy e.g 04-17-1992

      try:
        datetime.strptime("".join(dob.split("-")),'%m%d%Y').date()
      except ValueError,SyntaxError:
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
      #validate sex
      if sex not in sex_list:
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
      #validate password
      if(not password or len(password)> MAX_LENGTH_FIRST_LAST_PASS):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
      #validate phone us phone number
      phonePattern = re.match(r'^\d{3}-\d{3}-\d{4}$',cellphone)
      if phonePattern == None:
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
      #validate if driver boolean type
      if type(driver) is not bool:
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    return resp

def driver_check(rdata):
    license_no = rdata.get("license_no", "")
    license_exp = rdata.get("license_exp", "")
    car_make = rdata.get("car_make", "")
    car_type = rdata.get("car_type", "")
    car_mileage = rdata.get("car_mileage", "")
    max_passengers = rdata.get("max_passengers", "")
    resp = {"errCode":SUCCESS}

    if(not license_no or len(license_no)> MAX_LENGTH_FIRST_LAST_PASS):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    if(not car_make or len(car_make)> MAX_LENGTH_FIRST_LAST_PASS):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    if(not car_type or len(car_type)> MAX_LENGTH_FIRST_LAST_PASS):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    try:
        datetime.strptime("".join(license_exp.split("-")),'%m%d%Y').date()
    except ValueError,SyntaxError:
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH

    if type(car_mileage) is not int:
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    if type(max_passengers) is not int:
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    return resp


@csrf_exempt
def login(request):
    resp = {"errCode":SUCCESS}
    try:
        rdata = json.loads(request.body)
        resp= check_credentials(rdata)
        if resp["errCode"] == SUCCESS:
          email = rdata.get("email", "")
          password = rdata.get("password", "")
          try:
            u = User.objects.get(email =email,password = password)
            resp["errCode"] =SUCCESS
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
          except User.DoesNotExist:
            resp["errCode"] = ERR_NOT_USER
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
        else:
          return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    except KeyError:
        resp["errCode"] = ERR_BAD_KEY
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

def check_credentials(rdata):
  
  email = rdata.get("email", "")
  password = rdata.get("password", "")
  resp = {"errCode":SUCCESS}
  if not (email):
    resp["errCode"] = ERR_BAD_EMAIL
  if( len(email) > MAX_LENGTH_EMAIL):
    resp["errCode"] = ERR_BAD_EMAIL
  if(len(password)>MAX_LENGTH_FIRST_LAST_PASS):
    resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH

  return resp
@csrf_exempt
def filter(request):
    try:
        rdata = json.loads(request.body)
    except Exception, err:
        print str(err)

    resp = {"errCode":SUCCESS}
    eta = rdata.get("eta", "")
    etd = rdata.get("etd", "")
    depart_loc = rdata.get("depart_loc", "")
    arrive_loc = rdata.get("arrive_loc", "")
    #distance_proximity = rdata.get("distance_proximity", "") possibly of use in the future
    requested_etd = rdata.get("requested_etd", "")

    try:
        routes = Route.objects.all()
        rides = []
        for route in routes: 
            entry = route.to_dict()
            rides.append(entry)

        #algorithm here!

        resp["rides"] = rides
        resp["size"] = len(rides)
    except Exception, err:
            resp["errCode"] = ERR_DATABASE_SEARCH_ERROR
            resp["errMsg"] = str(err)
            print str(err)
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json") 

@csrf_exempt
def search(request):
    resp = {"errCode":SUCCESS}
    departloc = {}
    destloc = {}
    rdata = {}
    try:
        rdata = json.loads(request.body)
        departloc = rdata.get("depart-loc", "{}")
        destloc = rdata.get("dest-loc", "{}")
    except Exception, err:
        resp = {"errCode":ERR_BAD_JSON}
        print str(err)
    #TODO Parse json here.

    print rdata
    print departloc 
    print destloc
    date = rdata.get("date", "")
    departtime = rdata.get("time-depart", "")
    distThresh = int(rdata.get("dist-thresh", "50"))
    departlat = departloc.get("lat", "37.3041") #San Jose
    departlong = departloc.get("long", "121.8727") #San Jose
    destlat = destloc.get("lat", "37.3041")
    destlong = destloc.get("long", "121.8727")
    try:
        routes = Route.objects.all()
        rides = []
        for route in routes:
            #TODO filter routes to fit request.
            entry = route.to_dict()
            departDist = distance(float(departlat), float(departlong), float(entry.get("depart_lat","0")), float(entry.get("depart_lg","0")))
            #destDist = distance(float(destlat), float(destlon), float(entry.get("arrive_lat","0")), float(entry.get("arrive_lg","0")))
            if entry.get("status", "True") == "False":
                if departDist < distThresh: #and destDist < distThresh:
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

    departTime = rdata.get("edt", "")
    validDatums = handleRouteData(uid, departLocLong, departLocLat, destinationLocLong, destinationLocLat)
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
    r = request.GET
    route_id = r.get("route_id", -1)
    response = r.get("response", "") #-1) What is going on here? this is request right? Why do we have a response segment?
    print "route id: " + str(route_id)
    print "response: " + str(response)
    route = Route.objects.get(id=route_id)
    if response == "1":
        route.status="True"
        route.save()
    elif response == "0":
        route.status = "False"
        route.save()
    else:
        raise Exception("Invalid response" + str(response))
    
  except Exception, err:
    print str(err)
    return HttpResponse(json.dumps({'errCode':ERR_BAD_SERVER_RESPONSE}),content_type="application/json")

  return HttpResponse(json.dumps({'errCode':SUCCESS}),content_type="application/json")

#handles that coordinates are legit and uid exists in db
def handleRouteData(uid, departLocLong, departLocLat, destinationLocLong, destinationLocLat):
    if (len(departLocLat) > COORD_LENGTH_IN) | (len(departLocLong) > COORD_LENGTH_IN) | (not (90.0 >= float(departLocLat) >= -90.0)) | (not (180.0 >= float(departLocLong) >= -180.0)) :
		return ERR_BAD_DEPARTURE #-1
	
    if (len(destinationLocLong) > COORD_LENGTH_IN) | (len(destinationLocLat) > COORD_LENGTH_IN) | (not (90.0 >= float(destinationLocLat) >= -90.0)) | (not (180.0 >= float(destinationLocLong) >= -180.0)) :
        return ERR_BAD_DESTINATION #-2
	
    try:
        if not (DriverInfo.objects.get(id = uid)):
		return ERR_BAD_USERID #-3
    except Exception:
        return ERR_BAD_USERID #-3
    
    return SUCCESS

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

#from https://gist.github.com/rochacbruno/2883505
def distance(lat1, lon1, lat2, lon2):
    radius = 3959 #miles or 6371 km
 
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
 
    return d

@csrf_exempt
def deleteRides(request):
    resp = {"errCode":SUCCESS}
    Route.objects.all().delete()
    DriverInfo.objects.all().delete()
    User.objects.all().delete()
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

@csrf_exempt
def generateExamples(request):
    resp = {"errCode":SUCCESS}
    r = request.GET
    num = int(r.get("num", 0))
    resp['num'] = num
    for i in xrange(0,num):
        testUtils.genRide()
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
