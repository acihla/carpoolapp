from django.utils import simplejson as json
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import  send_mail,BadHeaderError
from validate_email import validate_email

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
ERR_EXPIRED_LICENSE =-15
ERR_REQUEST_EXISTS =-17
ERR_KEY_VAL_DOES_NOT_EXISTS =-18
ERR_BAD_APIKEY = -16
ERR_BAD_DRIVER_INFO = -19
#sample_date = "1992-04-17"

sex_list = ['male','female']

@csrf_exempt
def signup(request):
    resp = {"errCode":SUCCESS}
    try:
        rdata = json.loads(request.body)
        resp = sanitizeSignupData(rdata)
        #import pdb;pdb.set_trace()
        if resp["errCode"] == SUCCESS:
            firstname = rdata.get("firstname", "")
            lastname = rdata.get("lastname", "")
            email = rdata.get("email", None)
            dob = rdata.get("dob", "")
            sex = rdata.get("sex", "")
            #import pdb;pdb.set_trace()
            password = rdata.get("password", "")
            cellphone = rdata.get("cellphone", "")
            driver = rdata.get("driver", "0")

            date_obj = datetime.strptime("".join(dob.split("-")),'%m%d%Y').date()

            newUser = User(firstname = firstname, lastname = lastname, email = email, dob = date_obj, sex = sex, password = password, cellphone = cellphone, driver = driver)
            apikey = newUser.generate_apikey()
            newUser.apikey = apikey
            newUser.save()
            resp["apikey"] = apikey
            if (driver==1):
              print "im a driver"

              resp1 = driver_check(rdata)
              resp1["apikey"] = apikey
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
      is_valid = validate_email(email)

      if not is_valid:
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
      if (type(driver) is not bool) and (driver not in [0,1]):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    return resp

def driver_check(rdata):
    present = datetime.now().date()
    print "im in driver_check"
    license_no = rdata.get("license_no", "")
    license_exp = rdata.get("license_exp", "")
    car_make = rdata.get("car_make", "")
    car_type = rdata.get("car_type", "")
    car_mileage = rdata.get("car_mileage", "")
    max_passengers = rdata.get("max_passengers", "")
    resp = {"errCode":SUCCESS}

    if(not license_no or len(license_no)> MAX_LENGTH_FIRST_LAST_PASS):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
        print "license nomber toolong"
    if(not car_make or len(car_make)> MAX_LENGTH_FIRST_LAST_PASS):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
        print "car_make bad input"
    if(not car_type or len(car_type)> MAX_LENGTH_FIRST_LAST_PASS):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
        print "car_type bad input"
    try:
        exp_date=datetime.strptime("".join(license_exp.split("-")),'%m%d%Y').date() 
        #print "expiration date :" + exp_date
        #print "now :" + present
        print "exp_date " +str(exp_date)
        if exp_date < present:
           print "so u are expired"
           resp["errCode"]= ERR_EXPIRED_LICENSE
           print resp["errCode"]


    except ValueError,SyntaxError:
        print "in the except case"
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    #print "expiration date :" + exp_date
    #print "now :" + present

    #check if license expired
    #print present
    #if exp_date < present:
    #print "license expired"
    '''    print exp_date
        print present
        resp["errCode"] = ERR_EXPIRED_LICENSE
    '''
    
    if type(car_mileage) is not int:
        print "problem with mileage"
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    if type(max_passengers) is not int:
        print "problem with max_passenger"
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    print resp
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
            resp["errCode"] = SUCCESS
            resp["apikey"] = u.apikey
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
    departloc = ""
    destloc = ""
    rdata = {}
    try:
        rdata = json.loads(request.body)
    except Exception, err:
        resp = {"errCode":ERR_BAD_JSON}
        print str(err)
    #TODO Parse json here.
    departloc = json.loads(rdata.get("depart-loc", "{}"))
    destloc = json.loads(rdata.get("dest-loc", "{}"))
    print rdata
    print departloc 
    print destloc
    date = rdata.get("date", "")
    departtime = rdata.get("time-depart", "")
    distThresh = int(rdata.get("dist-thresh", "50"))
    departlat = departloc.get("lat", "37.3041") #San Jose
    departlong = departloc.get("long", "-121.8727") #San Jose
    destlat = destloc.get("lat", "37.3041")
    destlong = destloc.get("long", "-121.8727")

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
def getProfile(request):
    resp = {}
    rdata = json.loads(request.body)
    apikey = rdata.get("apikey", "")
    user = None
    try:
        user = User.objects.get(apikey = apikey)
        resp = user.to_dict()
        resp["errCode"] = SUCCESS
    except User.DoesNotExist:
            resp["errCode"] = ERR_BAD_APIKEY
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

    try:
        if user.driver:
            driver_info = DriverInfo.objects.get(driver=user.id)
            resp["driver_info"] = driver_info.to_dict()
    except DriverInfo.DoesNotExist:
        resp["errCode"] = ERR_BAD_DRIVER_INFO
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

@csrf_exempt
def addroute(request):
    rdata = json.loads(request.body)
    apikey = rdata.get("apikey", "")
    user = None
    try:
        user = User.objects.get(apikey = apikey)
    except User.DoesNotExist:
            resp["errCode"] = ERR_BAD_APIKEY
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

    #start = rdata.get("start", "")
    #end = rdata.get("end", "")

    departLocLong = rdata.get("depart-long", "")
    departLocLat = rdata.get("depart-lat", "")

    destinationLocLong = rdata.get("dest-long", "")
    destinationLocLat = rdata.get("dest-lat", "")
    departTime = rdata.get("edt", "")
    validDatums = handleRouteData(user.id, departLocLong, departLocLat, destinationLocLong, destinationLocLat)
    if (validDatums != 1):
    	resp = {"errCode" : validDatums}

    else:
        newRoute = Route(driver_info = User.objects.get(apikey=apikey), rider = None, depart_lat = departLocLat, depart_lg = departLocLong, arrive_lat = destinationLocLat, arrive_lg = destinationLocLong, depart_time = date_obj, status = False) #maps_info = directions, 
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
        apikey = data.get("apikey", "")
        user = None
        try:
            user = User.objects.get(apikey = apikey)
        except User.DoesNotExist:
            resp["errCode"] = ERR_BAD_APIKEY
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
        rider_id = user.id
        route_id = data['route_id']
        print route_id
        comment = data['comment']
        rider = User.objects.get(id=rider_id)
        route = Route.objects.get(id=route_id)
        driver_info =route.driver_info
        rider_email = rider.email
        print 'rider email is:' + rider_email
        driver_email = driver_info.driver.email
        driver_firstname = driver_info.driver.firstname
        driver_lastname  = driver_info.driver.lastname
        route.rider = rider
        route.save()
        print "before the try"
        try:
            print "right before i check"
            rq = ride_request.objects.get(rider=rider,route_id=route_id)
            if (rq.status=="Canceled"):
                status='Pending'
                request_ride(rider,route_id,status,comment)
                url = "http://127.0.0.1:8000/driver/accept"
                url += "?from=" + str(rider_id)
                url += "&to=" + str(driver_info.driver_id)
                url += "&route_id=" + str(route_id)
                yesUrl = url + "&response=1"
                noUrl = url + "&response=0"
                message = rider.firstname +" "+rider.lastname+ "would like a ride from you to accept, please click on the following link \n" + yesUrl + "\n to deny click, \n" + noUrl


            else:
                print "this is what i am returning"
                return HttpResponse(json.dumps({'errCode':ERR_REQUEST_EXISTS}),content_type="application/json")


        except ride_request.DoesNotExist:
            status='Pending' 
            request_ride(rider,route_id,status,comment)
            url = "http://127.0.0.1:8000/driver/accept"
            url += "?from=" + str(rider_id)
            url += "&to=" + str(driver_info.driver_id)
            url += "&route_id=" + str(route_id)
            yesUrl = url + "&response=1"
            noUrl = url + "&response=0"
            message = rider.firstname +" "+rider.lastname+ "would like a ride from you to accept, please click on the following link \n" + yesUrl + "\n to deny click, \n" + noUrl

    except KeyError:
        print "no it is actually this"
        return HttpResponse(json.dumps({'errCode':ERR_DATABASE_SEARCH_ERROR}),content_type="application/json")

    try:
        send_mail('Carpool Ride Notification',message,'carpoolcs169@gmail.com',['aimechicago@berkeley.edu'],fail_silently=False,auth_user=None ,auth_password=None, connection=None)

    except BadHeaderError:
        print "my fault is this"
        return HttpResponse(json.dumps({'errCode':ERR_BAD_HEADER}),content_type="application/json")
    print "then it worked"
    err= SUCCESS
    print err
    return HttpResponse(json.dumps({'errCode':err}),content_type="application/json")
@csrf_exempt
def accept_ride(request):
    try:
        print "at the begining of accept_ride"
        r = request.GET
        route_id = r.get("route_id", -1)
        response = r.get("response", "") #-1) What is going on here? this is request right? Why do we have a response segment?
        rider_id= r.get("from","")
        driver_id =r.get("to","")
        rider =User.objects.get(id=rider_id)
        rider_email = rider.email
        rider_firstname = rider.firstname
        rider_lastname= rider.lastname
        driver_info = DriverInfo.objects.get(driver_id=driver_id)
        driver_firstname= driver_info.driver.firstname
        driver_lastname= driver_info.driver.lastname
        print "route id: " + str(route_id)
        print "response: " + str(response)
        print "rider_email:" + rider_email
        print "rider_firstname:" + rider_firstname
        print "rider_lastname:" +  rider_lastname
        print "driver_firstname:"+ driver_firstname
        print "driver_lastname:" + driver_lastname
        route = Route.objects.get(id=route_id)
        print route
        print "let me see"
        if response == "1":
            print "ok response is true"
            route.status="True"
            route.save()
            message = "Congratulation " + rider_firstname +" " +rider_lastname+"\n" +"We would like to inform you that your trip is now confirmed with \n" + driver_firstname + " "+ driver_lastname

            comment = "I am really excited to have this ride"
            status  = 'Accepted'
            rq = ride_request.objects.get(rider =rider,route_id=route_id)
            rq.status = status
            rq.comment = comment
            rq.save()
            send_mail('Carpool Ride Notification',message,'carpoolcs169@gmail.com',['aimechicago@berkeley.edu'],fail_silently=False,auth_user=None ,auth_password=None, connection=None)

        elif response == "0":
            route.status = "False"
            route.save()
            message = "Sorry " + rider_firstname +" " +rider_lastname+"\n" +"We would like to inform you that the trip you selected with \n" + driver_firstname + " " +driver_lastname + "was denied please select another ride\n"
            comment = "I am sorry but I cannot ride with you"
            status  = 'Denied'
            rq = ride_request.objects.get(rider =rider,route_id=route_id)
            rq.status = status
            rq.comment = comment
            rq.save()
        
            send_mail('Carpool Ride Notification',message,'carpoolcs169@gmail.com',['aimechicago@berkeley.edu'],fail_silently=False,auth_user=None ,auth_password=None, connection=None)

        else:
            raise Exception("Invalid response" + str(response))
    
    except Exception, err:
        print "so i return bad response"
        print str(err)
        return HttpResponse(json.dumps({'errCode':ERR_BAD_SERVER_RESPONSE}),content_type="application/json")

    return HttpResponse(json.dumps({'errCode':SUCCESS}),content_type="application/json")  

def rides_accepted(request):
    return HttpResponse("Accepted")
    '''
    print "before the try in rides_accepted"
    try:
        print "in the begining of accepted"
        data = json.loads(request.raw_post_data)
        rider_id = data['rider_id']
        r_r = ride_request.objects.filter(rider_id=rider_id,status='Accepted') 
        dic_route ={}
        for a in r_r:
            r= Route.objects.get(pk=a.route_id)
            did= r.driver_info.id
            u=User.objects.get(pk=did)
            dic_route[a.route_id]= {
            'driver_firstname':u.firstname,
            'driver_lastname':u.lastname,
            'route_depart_lat':r.depart_lat,
            'route_depart_lg':r.depart_lg,
            'route_arrive_lat':r.arrive_lat,
            'route_arrive_lg':r.arrive_lg,
            'comment':a.comment,
            'departure_time':str(r.depart_time)
            }
        return HttpResponse(json.dumps(dic_route.values()),content_type="application/json")
    

    except KeyError:
        print "so there is a key error"
        return HttpResponse(json.dumps({'errCode':ERR_DATABASE_SEARCH_ERROR}),content_type="application/json")
    '''
@csrf_exempt
def rides_denied(request):
    print "in rides_denied"
    '''
    try:
        data = json.loads(request.raw_post_data)
        rider_id = data['rider_id']
        r_r = ride_request.objects.filter(rider_id=rider_id,status='Denied') 
        dic_route ={}
        for a in r_r:
            r= Route.objects.get(pk=a.route_id)
            did= r.driver_info.id
            u=User.objects.get(pk=did)
            dic_route[a.route_id]= {
            'driver_firstname':u.firstname,
            'driver_lastname':u.lastname,
            'route_depart_lat':r.depart_lat,
            'route_depart_lg':r.depart_lg,
            'route_arrive_lat':r.arrive_lat,
            'route_arrive_lg':r.arrive_lg,
            'comment':a.comment,
            'departure_time':str(r.depart_time)
            }
        return HttpResponse(json.dumps(dic_route.values()),content_type="application/json")
    

    except KeyError:
        return HttpResponse(json.dumps({'errCode':ERR_DATABASE_SEARCH_ERROR}),content_type="application/json")
    '''
@csrf_exempt
def rides_pending(request):
    #import pdb;pdb.set_trace()
    #return HttpResponse("Pending")
    
    print 'begining of pending' 
    try:
        print "in pending rides"
        data = json.loads(request.raw_post_data)
        rider_id = data['rider_id']
        r_r = ride_request.objects.filter(rider_id=rider_id,status='Pending')
        dic_route ={}
        for a in r_r:
            print "in the for loop"
            r= Route.objects.get(pk=a.route_id)
            did= r.driver_info.id
            u=User.objects.get(pk=did)
            dic_route[a.route_id]= {
            'driver_firstname':u.firstname,
            'driver_lastname':u.lastname,
            'route_depart_lat':r.depart_lat,
            'route_depart_lg':r.depart_lg,
            'route_arrive_lat':r.arrive_lat,
            'route_arrive_lg':r.arrive_lg,
            'comment':a.comment,
            'departure_time':str(r.depart_time)
            }
        return HttpResponse(json.dumps(dic_route.values()),content_type="application/json")
    

    except KeyError:
        return HttpResponse(json.dumps({'errCode':ERR_DATABASE_SEARCH_ERROR}),content_type="application/json")
    
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

def request_ride(rider,route_id,status='Pending',comment=''):
    rq= ride_request(rider =rider,route_id =route_id,status=status,comment=comment)
    rq.save()

def can_ride(rider,route_id,status='',comment=''):
    can_rq = ride_request(rider=rider,route_id=route_id,status=status,comment=comment)
    can_rq.save()

@csrf_exempt
def cancel_ride(request):
    try:
        data = json.loads(request.raw_post_data)
        rider_id = data['rider_id']
        route_id = data['route_id']
        rider = User.objects.get(id=rider_id)
        try:
            print "right before i check"
            rq = ride_request.objects.get(rider=rider,route_id=route_id)
            if (rq.status=="Pending" or rq.status=="Accepted"):
                status="Canceled"
                comment ="Sorry but i changed my mind"
                can_ride(rider,route_id,status,comment)
            else:
                print "either your ride was denied or you canceled it"

        except ride_request.DoesNotExist:
            return HttpResponse(json.dumps({'errCode':ERR_KEY_VAL_DOES_NOT_EXISTS}),content_type="application/json")
     
            
        return HttpResponse(json.dumps({'errCode':SUCCESS}),content_type="application/json")


    except KeyError:
        return HttpResponse(json.dumps({'errCode':ERR_DATABASE_SEARCH_ERROR}),content_type="application/json")



