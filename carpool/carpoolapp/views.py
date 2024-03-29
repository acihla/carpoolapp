
	

from django.utils import simplejson as json
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail,BadHeaderError
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
import unitTest
from googlemaps import GoogleMaps
from datetime import *
import math

#connecting using api key for alex.cihla@gmail.com
gmaps = GoogleMaps("AIzaSyAGf-Mbj40HtzmRmOvPWZX4RnE2RIG_tzc")

#responses to be handled by application
SUCCESS = 1 # : a success
ERR_BAD_DEPARTURE = -1 # : Departure location is not valid
ERR_BAD_DESTINATION = -2 # : Destination location is not valid
ERR_BAD_USERID = -3 # : UID does not exist in db, or is not a driver
ERR_BAD_TIME = -4 #format for time is bad
ERR_DATABASE_SEARCH_ERROR = -5
ERR_BAD_HEADER= -6
ERR_BAD_SERVER_RESPONSE = -7
MAX_LENGTH_IN = 200 #max length for all datums in our db
MAX_LENGTH_FIRST_LAST_PASS = 15 #max length for first and last name and password
MAX_LENGTH_EMAIL = 50 #max length email
COORD_LENGTH_IN = 20 # max length of coordinates
ERR_BAD_KEY = -8
ERR_NOT_USER = -9
ERR_BAD_EMAIL = -10
ERR_BAD_INPUT_OR_LENGTH = -11
ERR_BAD_DOB = -12
ERR_BAD_JSON = -13
ERR_USER_EXISTS =-14
ERR_EXPIRED_LICENSE =-15
ERR_BAD_APIKEY = -16
ERR_REQUEST_EXISTS =-17
ERR_KEY_VAL_DOES_NOT_EXISTS =-18
ERR_BAD_DRIVER_INFO = -19
ERR_BAD_CREDENTIALS = -20
ERR_UNKOWN_IN_SIGNUP = -21
ERR_UNKNOWN_ROUTE = -22
ERR_NO_RIDER_DRIVER_CONTACT =-23
ERR_BAD_PASSWORD = -24
ERR_SEE_ERR_MSG = -25
ERR_UNKNOWN_DRIVER =-26
#sample_date = "1992-04-17"

class request:
    body = {}

sex_list = ['male','female']

@csrf_exempt
def signup(request):
    resp = {"errCode":ERR_UNKOWN_IN_SIGNUP}
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
            driver = rdata.get("driver", 0)

            date_obj = datetime.strptime("".join(dob.split("-")),'%m%d%Y').date()

            phonePattern = re.compile(r'''
# don't match beginning of string, number can start anywhere
(\d{3}) # area code is 3 digits (e.g. '800')
\D* # optional separator is any number of non-digits
(\d{3}) # trunk is 3 digits (e.g. '555')
\D* # optional separator
(\d{4}) # rest of number is 4 digits (e.g. '1212')
\D* # optional separator
(\d*) # extension is optional and can be any number of digits
$ # end of string
''', re.VERBOSE)
            phonedict = phonePattern.search(cellphone).groups()
            cellphone = "".join(phonedict)
            newUser = User(firstname = firstname, lastname = lastname, email = email, dob = date_obj, sex = sex, password = password, cellphone = cellphone, user_type = driver)
            apikey = newUser.generate_apikey()
            newUser.apikey = apikey
            resp["apikey"] = apikey
            newUser.save()

            if driver == 1:
                #print "im a driver"
                resp1 = driver_check(rdata)
                if resp1["errCode"]== SUCCESS:
                    resp1["apikey"] = apikey
                    license_no = rdata.get("license_no", "")
                    license_exp = rdata.get("license_exp", "")
                    car_make = rdata.get("car_make", "")
                    car_type = rdata.get("car_type", "")
                    car_mileage = rdata.get("car_mileage", "")
                    max_passengers = str(rdata.get("max_passengers", 0))
                    license_date_obj = datetime.strptime("".join(license_exp.split("-")),'%m%d%Y').date()
                    try:
                        newDriverInfo = DriverInfo(driver = newUser, license_no = license_no, license_exp = license_date_obj, car_make = car_make, car_type = car_type, car_mileage = car_mileage, max_passengers = max_passengers)
                        newDriverInfo.save()
                        #print "the driver was saved!"
                    except Exception, err:
                        print str(err)
                        User.objects.get(id=newUser.id).delete()
                        resp = {"errCode:" : ERR_UNKOWN_IN_SIGNUP}
                else:
                    return HttpResponse(json.dumps(resp1, cls=DjangoJSONEncoder), content_type = "application/json")
            
        else:
          return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    except Exception, err:
        print str(err)
        resp = {"errCode:" : str(rdata)} #ERR_UNKOWN_IN_SIGNUP}

    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

def sanitizeSignupData(rdata):
    firstname = rdata.get("firstname", "")
    lastname = rdata.get("lastname", "")
    email = rdata.get("email", None)
    dob = rdata.get("dob", "")
    sex = rdata.get("sex", "")
    password = rdata.get("password", "")
    cellphone = rdata.get("cellphone", "")
    driver = rdata.get("driver", 0)
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
        
      '''
phonePattern = re.match(r'^\d{3}-\d{3}-\d{4}$',cellphone)
phonePattern2 = re.match(r'^\d{10}$',cellphone)
if phonePattern == None and phonePattern2 == None:
resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
'''
      #validate if driver boolean type
      if (type(driver) is not int) and (driver not in [0,1]):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    return resp

def driver_check(rdata):
    present = datetime.now().date()
    #print "im in driver_check"
    license_no = rdata.get("license_no", "")
    license_exp = rdata.get("license_exp", "")
    car_make = rdata.get("car_make", "")
    car_type = rdata.get("car_type", "")
    car_mileage = rdata.get("car_mileage", "")
    max_passengers = rdata.get("max_passengers", 0)
    resp = {"errCode":SUCCESS}

    if(not license_no or len(license_no)> MAX_LENGTH_FIRST_LAST_PASS):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
        #print "license nomber toolong"
    if(not car_make or len(car_make)> MAX_LENGTH_FIRST_LAST_PASS):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
        #print "car_make bad input"
    if(not car_type or len(car_type)> MAX_LENGTH_FIRST_LAST_PASS):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
        #print "car_type bad input"
    try:
        exp_date=datetime.strptime("".join(license_exp.split("-")),'%m%d%Y').date()
        #print "expiration date :" + exp_date
        #print "now :" + present
        #print "exp_date " +str(exp_date)
        if exp_date < present:
           #print "so u are expired"
           resp["errCode"]= ERR_EXPIRED_LICENSE
           print resp["errCode"]


    except ValueError,SyntaxError:
        #print "in the except case"
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    #print "expiration date :" + exp_date
    #print "now :" + present

    #check if license expired
    #print present
    #if exp_date < present:
    #print "license expired"
    ''' print exp_date
print present
resp["errCode"] = ERR_EXPIRED_LICENSE
'''
    
    if type(car_mileage) is not int:
        #print "problem with mileage"
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    if type(max_passengers) is not int:
        #print "problem with max_passenger"
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
            u = User.objects.get(email =email)
            
            if u.password == password:
                resp["errCode"] = SUCCESS
                resp["apikey"] = u.apikey
                return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
            else:
                resp["errCode"] = ERR_BAD_PASSWORD
                resp["apikey"] = "None"
                return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
          except User.DoesNotExist:
            resp["errCode"] = ERR_NOT_USER
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
        else:
          return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    except Exception:
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
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

    #TODO Parse json here.
    departloc = rdata.get("depart-loc", {})
    destloc = rdata.get("dest-loc", {})
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
            if entry.get("status", "invalid") == "valid" and entry.get("available_seats", 0) > 0:
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
def manageRoute(request):
    resp = {}
    rdata = json.loads(request.body)
    apikey = rdata.get("apikey", "")
    user = None
    try:
        user = User.objects.get(apikey = apikey)
        resp["errCode"] = SUCCESS
    except User.DoesNotExist:
            resp["errCode"] = ERR_BAD_APIKEY
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    try:
        if user.user_type == 1:
            driver_info = DriverInfo.objects.get(driver=user.id)
            routes = Route.objects.filter(driver_info = driver_info)
            routes_dict = []
            for route in routes:
                routes_dict.append(route.to_dict())
            resp["rides"] = routes_dict
            resp['size'] = len(routes_dict)
        else:
            resp["errCode"] = ERR_BAD_DRIVER_INFO
    except DriverInfo.DoesNotExist:
        resp["errCode"] = ERR_BAD_DRIVER_INFO
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

@csrf_exempt
def manageRequest(request):
    resp = {}
    rdata = json.loads(request.body)
    apikey = rdata.get("apikey", "")
    user = None
    try:
        user = User.objects.get(apikey = apikey)
        resp["errCode"] = SUCCESS
        #print("this is the user type!!!!!" + str(user.user_type))
        if user.user_type == 1:
            driver_info = DriverInfo.objects.get(driver=user.id)
            driver_requests = ride_request.objects.filter(driver_apikey = user.apikey)
            requests = []
            for request in driver_requests:
                if request.status != "Cancelled":
                    req = request.to_dict()
                    try:
                        route = Route.objects.get(id=request.route_id)
                        req["route"] = route.to_dict()
                    except Exception, err:
                        req["route"] = "Cancelled"
                        
                    rider = User.objects.get(apikey = request.rider_apikey)
                    if rider is None:
                        resp["errMsg"] = "rider is None"
                        resp["errCode"] = ERR_SEE_ERR_MSG
                    else:
                        req["rider"] = rider.to_dict()
                    requests.append(req)
            resp["requests"] = requests
            resp['size'] = len(requests)
        elif user.user_type == 0:
            resp["errCode"] = ERR_SEE_ERR_MSG
            resp["errMsg"] = "Not a driver"
        else:
            resp["errCode"] = ERR_BAD_APIKEY
    except User.DoesNotExist:
            resp["errCode"] = ERR_BAD_APIKEY
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    except ride_request.DoesNotExist:
        resp["errCode"] = SUCCESS
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")


@csrf_exempt
def managePendingRequest(request):
    resp = {}
    rdata = json.loads(request.body)
    apikey = rdata.get("apikey", "")
    user = None
    try:
        user = User.objects.get(apikey = apikey)
        resp["errCode"] = SUCCESS
        rider_requests = ride_request.objects.filter(rider_apikey=apikey)
        requests = []
        for request in rider_requests:
            if request.status == "Pending":
                req = request.to_dict()
                route = Route.objects.get(id=request.route_id)
                if route is None:
                    resp["errMsg"] =  "route is None"
                    resp["errCode"] = ERR_SEE_ERR_MSG
                else:
                    req["route"] = route.to_dict()

                rider = User.objects.get(apikey = request.rider_apikey)
                if rider is None:
                    resp["errMsg"] = "rider is None"
                    resp["errCode"] = ERR_SEE_ERR_MSG
                else:
                    req["rider"] = rider.to_dict()
                requests.append(req)
        resp["requests"] = requests
        resp['size'] = len(requests)

    except User.DoesNotExist:
            resp["errCode"] = ERR_BAD_APIKEY
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    except ride_request.DoesNotExist:
        resp["errCode"] = SUCCESS
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")


@csrf_exempt
def manageAcceptedRequest(request):
    resp = {}
    rdata = json.loads(request.body)
    apikey = rdata.get("apikey", "")
    user = None
    try:
        user = User.objects.get(apikey = apikey)
        resp["errCode"] = SUCCESS
        rider_requests = ride_request.objects.filter(rider_apikey=apikey)
        requests = []
        for request in rider_requests:
            if request.status == "Accepted":
                req = request.to_dict()
                route = Route.objects.get(id=request.route_id)
                if route is None:
                    resp["errMsg"] =  "route is None"
                    resp["errCode"] = ERR_SEE_ERR_MSG
                else:
                    req["route"] = route.to_dict()

                rider = User.objects.get(apikey = request.rider_apikey)
                if rider is None:
                    resp["errMsg"] = "rider is None"
                    resp["errCode"] = ERR_SEE_ERR_MSG
                else:
                    req["rider"] = rider.to_dict()
                requests.append(req)
        resp["requests"] = requests
        resp['size'] = len(requests)

    except User.DoesNotExist:
            resp["errCode"] = ERR_BAD_APIKEY
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    except ride_request.DoesNotExist:
        resp["errCode"] = SUCCESS
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
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
        if user.user_type == 1:
            driver_info = DriverInfo.objects.get(driver=user.id)
            resp["driver_info"] = driver_info.to_dict()
    except DriverInfo.DoesNotExist:
        resp["errCode"] = ERR_BAD_DRIVER_INFO
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

@csrf_exempt
def changePassword(request):
    resp = {}
    rdata = json.loads(request.body)
    apikey = rdata.get("apikey", "")
    currentpw = rdata.get("currentpw", "")
    newpw = rdata.get("newpw", "")
    email = rdata.get("email", "")
    user = None
    try:
        user = User.objects.get(apikey = apikey)
        if user.password == currentpw and user.email == email:
            if(not newpw or len(newpw)> MAX_LENGTH_FIRST_LAST_PASS):
                resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
            else:
                #change pw here
                user.password = newpw
                user.save()
                resp["errCode"] = SUCCESS
        else:
            resp["errCode"] = ERR_BAD_CREDENTIALS
    except User.DoesNotExist:
            resp["errCode"] = ERR_BAD_APIKEY
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")


def sanitizeChangeUserInfoData(rdata):
    firstname = rdata.get("firstname", "")
    lastname = rdata.get("lastname", "")
    email = rdata.get("email", None)
    dob = rdata.get("dob", "")
    sex = rdata.get("sex", "")
    cellphone = rdata.get("cellphone", "")
    driver = rdata.get("driverOrNot", 0)
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
      #validate if driver boolean type
      if (type(driver) is not int) and (driver not in [0,1]):
        resp["errCode"] = ERR_BAD_INPUT_OR_LENGTH
    return resp

@csrf_exempt
def changeUserInfo(request):
    resp = {}
    rdata = json.loads(request.body)
    errCode = sanitizeSignupData(rdata)
    resp["errCode"] = errCode

    if errCode == SUCCESS:
        user = None
        try:
            apikey = rdata.get("apikey", "")
            user = User.objects.get(apikey = apikey)
            
            cellphone = rdata.get("cellphone","")
            dob = rdata.get("dob","")
            date_obj = datetime.strptime("".join(dob.split("-")),'%m%d%Y').date()

            phonePattern = re.compile(r'''
# don't match beginning of string, number can start anywhere
(\d{3}) # area code is 3 digits (e.g. '800')
\D* # optional separator is any number of non-digits
(\d{3}) # trunk is 3 digits (e.g. '555')
\D* # optional separator
(\d{4}) # rest of number is 4 digits (e.g. '1212')
\D* # optional separator
(\d*) # extension is optional and can be any number of digits
$ # end of string
''', re.VERBOSE)
            phonedict = phonePattern.search(cellphone).groups()
            cellphone = "".join(phonedict)

            user.firstname = rdata.get("firstname","")
            user.lastname = rdata.get("lastname","")
            user.sex = rdata.get("sex","")
            user.email = rdata.get("email","")
            user.cellphone = cellphone
            user.dob = date_obj
            user.user_type = rdata.get("driverOrNot", 0)
            user.save()
            resp["errCode"] = SUCCESS
        except User.DoesNotExist:
                resp["errCode"] = ERR_BAD_APIKEY
                return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

@csrf_exempt
def changeDriverInfo(request):
    resp = {}
    rdata = json.loads(request.body)
    errCode = driver_check(rdata)
    resp["errCode"] = errCode

    if errCode == SUCCESS:
        try:
            apikey = rdata.get("apikey", "")
            user = User.objects.get(apikey = apikey)
            driver_info = DriverInfo.objects.get(driver = user)
            
            driver_info.license_no = rdata.get("license_no", "")
            driver_info.car_make = rdata.get("car_make", "")
            driver_info.car_type = rdata.get("car_type", "")
            driver_info.car_mileage = rdata.get("car_mileage", 0)
            driver_info.max_passengers = str(rdata.get("max_passengers", 0))
            license_exp = rdata.get("license_exp", "")
            driver_info.license_exp = datetime.strptime("".join(license_exp.split("-")),'%m%d%Y').date()
            driver_info.save()

            resp["errCode"] = SUCCESS
        except User.DoesNotExist:
                resp["errCode"] = ERR_BAD_APIKEY
                return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

@csrf_exempt
def getTestDriver(request):
    #resp = {}
    #estDriver = testLib.makeRequest("/signup", method="POST", data = {'firstname':'AJ','lastname':'Cihla','email':'alex.samuel@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':1,'license_no':'blahblahbla','license_exp':'05-15-2017','car_make':'','car_type':'sedan','car_mileage':100000,'max_passengers':2} )
    #resp["apikey"] = testDriver.apikey
    try:
        testDriver = User.objects.get(email = "alex.samuel@yahoo.com")
        resp["apikey"] = testDriver.apikey
    except User.DoesNotExist:
        resp["apikey"] = "None"
        
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

@csrf_exempt
def addroute(request):
    rdata = json.loads(request.body)
    print(rdata)
    apikey = rdata.get("apikey", "")
    user = None
    resp = {"errCode" : SUCCESS}
    try:
        user = User.objects.get(apikey = apikey)
        departLocLong = rdata.get("depart-long", "")
        departLocLong = departLocLong[:14]
        departLocLat = rdata.get("depart-lat", "")
        departLocLat = departLocLat[:14]
        destinationLocLong = rdata.get("dest-long", "")
        destinationLocLong = destinationLocLong[:14]
        destinationLocLat = rdata.get("dest-lat", "")
        destinationLocLat = destinationLocLat[:14]
        try:
            departTime = rdata.get("edt", "")
            departDate = rdata.get("date","")
            departTime = departTime.strip()
            departDate = departDate.strip()
            departDate = datetime.strptime("".join(departDate.split("-")),'%m%d%Y')
            hhmm = departTime.split(':')
            date_obj = departDate + timedelta(hours= int(hhmm[0]), minutes= int(hhmm[1]))
            #date_obj = datetime.combine(departDate, departTime)
        except Exception, err:
            print str(err)
            print departDate
            print departTime

        validDatums = handleRouteData(user.id, departLocLong, departLocLat, destinationLocLong, destinationLocLat)
        if (validDatums != 1):
            resp = {"errCode" : validDatums}

        else:
            try:
                driver_info = DriverInfo.objects.get(driver= User.objects.get(apikey=apikey))
                newRoute = Route(driver_info = driver_info, depart_lat = departLocLat, depart_lg = departLocLong, arrive_lat = destinationLocLat, arrive_lg = destinationLocLong, depart_time = date_obj, status = "valid", available_seats = int(driver_info.max_passengers)) #maps_info = directions,
                newRoute.save()
                resp = {"errCode" : SUCCESS}

            except DriverInfo.DoesNotExist:
                resp = {}
                resp["errCode"] = ERR_BAD_APIKEY
                return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    except User.DoesNotExist:
        resp = {}
        resp["errCode"] = ERR_BAD_APIKEY
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
    except Exception, err:
        print "so i return bad response"
        print str(err)
        return HttpResponse(json.dumps({'errCode':ERR_BAD_SERVER_RESPONSE}),content_type="application/json")


    #start = rdata.get("start", "")
    #end = rdata.get("end", "")

    
        
        
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

#request ride function
@csrf_exempt
def select_ride(request):
    try:
        data = json.loads(request.body)
        apikey = data.get("apikey", "")
        user = None
        route_id = data.get("route_id",-1)
        departloc = data.get("depart-loc", {})
        destloc = data.get("dest-loc", {})

        rider_departlat= departloc.get("lat", "0")[:14]
        rider_departlong = departloc.get("long", "0")[:14]
        rider_destlat = destloc.get("lat", "0")[:14]
        rider_destlong = destloc.get("long", "0")[:14]
        date = data.get("date", "")
        rider_departtime = data.get("time-depart", "")

        print str(rider_departtime)
        print "rider depart_lat " + str(rider_departlat)

        try:
            #print "in the try for user_exist"
            user = User.objects.get(apikey = apikey)
            #print "after getting user"
            rider = user
            #print "im after route_id"
            rider_email = rider.email
            #print 'rider email is:' + rider_email
            #print "before user doesnotexist ecxception"
        except User.DoesNotExist:
            resp={}
            resp["errCode"] = ERR_BAD_APIKEY
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
        try:
            #print "try for bad route_id"
            route = Route.objects.get(id=route_id)
            #print route_id
            driver_info =route.driver_info
            driver_email = driver_info.driver.email
            driver_firstname = driver_info.driver.firstname
            driver_lastname = driver_info.driver.lastname

        except Route.DoesNotExist:
            err = ERR_UNKNOWN_ROUTE
            return HttpResponse(json.dumps({'errCode':err}),content_type="application/json")
        try:
            rq = ride_request.objects.get(rider_apikey=apikey,route_id=route_id)
            if (rq.status=="Cancelled"):
                status='Pending'
                request_ride(apikey,route_id,str(rider_departlat),str(rider_departlong),str(rider_destlat),str(rider_destlong),str(rider_departtime),status)
                '''url = "http://carpool1691.herokuapp.com/driver/accept"
                url += "?from=" + apikey
                url += "&to=" + str(driver_info.driver_id)
                url += "&route_id=" + str(route_id)
                yesUrl = url + "&response=1"
                noUrl = url + "&response=0"
                '''
                message = rider.firstname +" "+rider.lastname+ " would like a ride from you to accept or deny please check your account"

                '''loc_url = "http://127.0.0.1:8000/driver/accept"
                loc_url += "?from=" + apikey
                loc_url += "&to=" + str(driver_info.driver_id)
                loc_url += "&route_id=" + str(route_id)
                loc_yesUrl = loc_url + "&response=1"
                loc_noUrl = loc_url + "&response=0"
                loc_message = rider.firstname +" "+rider.lastname+ "would like a ride from you to accept, please click on the following link \n" + loc_yesUrl + "\n to deny click, \n" + loc_noUrl
                '''

            else:
                return HttpResponse(json.dumps({'errCode':ERR_REQUEST_EXISTS}),content_type="application/json")


        except ride_request.DoesNotExist:
            status='Pending'
            request_ride(apikey,route_id,str(rider_departlat),str(rider_departlong),str(rider_destlat),str(rider_destlong),str(rider_departtime),status)
            '''url = "http://carpool1691.herokuapp.com/driver/accept"
            url += "?from=" + apikey
            url += "&to=" + str(driver_info.driver_id)
            url += "&route_id=" + str(route_id)
            yesUrl = url + "&response=1"
            noUrl = url + "&response=0"
            '''
            message = rider.firstname +" "+rider.lastname+ " would like a ride from you to accept or deny, please visit your account"
            '''
            loc_url = "http://127.0.0.1:8000/driver/accept"

            loc_url += "?from=" + apikey
            loc_url += "&to=" + str(driver_info.driver_id)
            loc_url += "&route_id=" + str(route_id)
            loc_yesUrl = loc_url + "&response=1"
            loc_noUrl = loc_url + "&response=0"
            loc_message = rider.firstname +" "+rider.lastname+ "would like a ride from you to accept, please click on the following link \n" + loc_yesUrl + "\n to deny click, \n" + loc_noUrl
            '''
    except KeyError:
        return HttpResponse(json.dumps({'errCode':ERR_DATABASE_SEARCH_ERROR}),content_type="application/json")

    try:
        send_mail('Carpool Ride Notification',message,'carpoolcs169@gmail.com',[driver_email,'aimechicago@berkeley.edu'],fail_silently=False,auth_user=None ,auth_password=None, connection=None)

        #send_mail('Carpool Ride Notification',loc_message,'carpoolcs169@gmail.com',[driver_email,'aimechicago@berkeley.edu'],fail_silently=False,auth_user=None ,auth_password=None, connection=None)

    except BadHeaderError:
        print "my fault is this"
        return HttpResponse(json.dumps({'errCode':ERR_BAD_HEADER}),content_type="application/json")

    return HttpResponse(json.dumps({'errCode':SUCCESS}),content_type="application/json")

@csrf_exempt
def accept_ride(request):
    print "in accept_ride"
    try:
        r = json.loads(request.body)
        request_id = r.get("request_id", -1)
        driver_api =r.get("driver_api","")
        response = r.get("response", -1) #0 to deny request, 1 to accept it 
        #rider_api= r.get("rider_api","")

        try:
            request = ride_request.objects.get(id=request_id)
        except ride_request.DoesNotExist:
            err = ERR_UNKNOWN_ROUTE
            return HttpResponse(json.dumps({'errCode':err}),content_type="application/json")
        
        try:
            driver_info = User.objects.get(apikey=driver_api)
            driver_firstname= driver_info.firstname
            driver_lastname= driver_info.lastname

        except User.DoesNotExist:
            err = ERR_BAD_APIKEY
            return HttpResponse(json.dumps({'errCode':err}),content_type="application/json")
        
        '''
        try:

            rider =User.objects.get(apikey=rider_apikey)
            print 'rider_apikey: ' + rider_apikey
            rider_email = rider.email
            rider_firstname = rider.firstname
            rider_lastname= rider.lastname

        except User.DoesNotExist:
            resp={}
            resp["errCode"] = ERR_BAD_APIKEY
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")
        

        print "route id: " + str(route_id)
        print "response: " + str(response)
        print "rider_email:" + rider_email
        print "rider_firstname:" + rider_firstname
        print "rider_lastname:" + rider_lastname
        print "driver_firstname:"+ driver_firstname
        print "driver_lastname:" + driver_lastname
        '''

        if response == 1:
            '''
            print "in response 1"
            message = "Congratulation " + rider_firstname +" " +rider_lastname+"\n" +"We would like to inform you that your trip is now confirmed with \n" + driver_firstname + " "+ driver_lastname
            '''

            status = 'Accepted'
            rq = ride_request.objects.get(id=request_id)
            rq.status = status
            rq.save()
            #send_mail('Carpool Ride Notification',message,'carpoolcs169@gmail.com',[rider_email,'aimechicago@berkeley.edu'],fail_silently=False,auth_user=None ,auth_password=None, connection=None)

        elif response == 0:
            '''
            message = "Sorry " + rider_firstname +" " +rider_lastname+"\n" +"We would like to inform you that the trip you selected with \n" + driver_firstname + " " +driver_lastname + "was denied please select another ride\n"
            status = 'Denied'
            '''
            status = 'Denied'
            rq = ride_request.objects.get(id=request_id)
            rq.status = status
            rq.save()
        
            #send_mail('Carpool Ride Notification',message,'carpoolcs169@gmail.com',['aimechicago@berkeley.edu',rider_email],fail_silently=False,auth_user=None ,auth_password=None, connection=None)

        else:
            raise Exception("Invalid response " + str(response))
    
    except Exception, err:
        print str(err)
        return HttpResponse(json.dumps({'errCode':str(ERR_BAD_SERVER_RESPONSE)}),content_type="application/json")

    return HttpResponse(json.dumps({'errCode':SUCCESS}),content_type="application/json") 
'''
def rides_accepted(request):
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
@csrf_exempt
def rides_denied(request):
    
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

'''
def request_ride(rider_apikey,route_id,rider_departlat,rider_departlong,rider_destlat,rider_destlong,rider_departtime,status='Pending'):
    rq= ride_request(rider_apikey =rider_apikey,route_id =route_id,status=status,depart_lat=rider_departlat,depart_lg=rider_departlong,arrive_lat=rider_destlat,depart_time=rider_departtime,arrive_lg=rider_destlong)
    dr = Route.objects.get(id=route_id)
    dr_info = dr.driver_info
    dr_id = dr_info.driver_id
    u = User.objects.get(id= dr_id)
    dr_apikey = u.apikey
    rq.driver_apikey=dr_apikey
    rq.save()

@csrf_exempt
def delete_route(request):
    try:
        resp = {}
        data = json.loads(request.body)
        apikey = data['apikey']
        route_id = data['route_id']
        route_to_delete = Route.objects.get(id = route_id)
        if (route_to_delete.driver_info.driver.apikey == apikey):
            '''affected_riders = ride_request.objects.get(route_id = route_id)
for rr in affected_riders:
#send email to riders that have requests to this cancelled ride
rider_to_notify = User.objects.get(apikey = rr.rider_apikey)
rider_email = rider_to_notify.email
message = "A route that you have requested has been cancelled by the driver! We are sorry for any inconvenience that this may have caused you. Please check your scheduled rendezvous and find a new ride." #rider.firstname +" "+rider.lastname+ "would like a ride from you to accept, please click on the following link \n" + yesUrl + "\n to deny click, \n" + noUrl
try:
send_mail('Carpool Ride Notification',message,'carpoolcs169@gmail.com',[rider_email,'aimechicago@berkeley.edu'],fail_silently=False,auth_user=None ,auth_password=None, connection=None)

except BadHeaderError:
print "The delete route notification system has failed"
return HttpResponse(json.dumps({'errCode':ERR_BAD_HEADER}),content_type="application/json")
'''
            route_to_delete.delete()
            resp["errCode"] = SUCCESS
        else:
            print(route_to_delete.driver_info.driver.apikey)
            print(apikey)
            resp["errCode"] = ERR_BAD_CREDENTIALS

        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

    except Exception,err:
        print(err)
        resp["errCode"] = ERR_BAD_APIKEY
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")


@csrf_exempt
def cancel_request(request):
    try:
        data = json.loads(request.body)
        apikey= data['apikey']
        route_id = data['route_id']
        try:
            route = Route.objects.get(id=route_id)
        except Route.DoesNotExist:
            err = ERR_UNKNOWN_ROUTE
            return HttpResponse(json.dumps({'errCode':err}),content_type="application/json")

        print route.available_seats
        try:

            rider =User.objects.get(apikey=apikey)

        except User.DoesNotExist:
            resp={}
            resp["errCode"] = ERR_BAD_APIKEY
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")


        try:
            rq = ride_request.objects.get(rider_apikey=apikey,route_id=route_id)
            if (rq.status=="Pending" or rq.status=="Accepted"):
                status="Canceled"
                rq.status=status
                rq.save()
                if (rq.status == "Accepted"):
                    route.available_seats +=1
                route.save()
                print route.available_seats

        except ride_request.DoesNotExist:
            return HttpResponse(json.dumps({'errCode':ERR_NO_RIDER_DRIVER_CONTACT}),content_type="application/json")
        return HttpResponse(json.dumps({'errCode':SUCCESS}),content_type="application/json")


    except KeyError:
        return HttpResponse(json.dumps({'errCode':ERR_DATABASE_SEARCH_ERROR}),content_type="application/json")

    
#handles that coordinates are legit and uid exists in db
def handleRouteData(uid, departLocLong, departLocLat, destinationLocLong, destinationLocLat):
    
    if (len(departLocLat) > COORD_LENGTH_IN) | (len(departLocLong) > COORD_LENGTH_IN) | (not (90.0 >= float(departLocLat) >= -90.0)) | (not (180.0 >= float(departLocLong) >= -180.0)) :
        return ERR_BAD_DEPARTURE #-1
    
    if (len(destinationLocLong) > COORD_LENGTH_IN) | (len(destinationLocLat) > COORD_LENGTH_IN) | (not (90.0 >= float(destinationLocLat) >= -90.0)) | (not (180.0 >= float(destinationLocLong) >= -180.0)) :
        return ERR_BAD_DESTINATION #-2
    
    try:
        if not (User.objects.get(id = uid)):
            return ERR_BAD_USERID #-3
    except Exception:
        return ERR_BAD_USERID #-3
    
    return SUCCESS


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
    r = json.loads(request.body)
    num = int(r.get("num", 0))
    resp['num'] = num
    for i in xrange(0,num):
        testUtils.genRide()
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")


    
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


@csrf_exempt
def leave_feedback(request):
    print "top of leave feedback"
    
    try:
        data = json.loads(request.body)
        apikey= data['apikey']
        route_id = data['route_id']
        try:
            route= Route.objects.get(id=route_id)
            driver_info = route.driver_info
            driver =driver_info.driver
            owner_apikey = driver.apikey
        except Route.DoesNotExist:
            err = ERR_UNKNOWN_ROUTE
            return HttpResponse(json.dumps({'errCode':err}),content_type="application/json")
        try:
            author =User.objects.get(apikey= apikey)
            author_name = author.firstname + " " + author.lastname
        except User.DoesNotExist:
            resp={}
            resp["errCode"] = ERR_BAD_APIKEY
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

        rating = data['rating']
        if type(rating) != type(int):
            return HttpResponse(json.dumps({'errCode':ERR_BAD_INPUT_OR_LENGTH}),content_type="application/json")


        comment = data['comment']
        if not isinstance(comment, str):
            return HttpResponse(json.dumps({'errCode':ERR_BAD_INPUT_OR_LENGTH}),content_type="application/json")

        try:
            print "in the try"
            ride_request.objects.get(rider_apikey=apikey,route_id=route_id)
            fback = Rating(owner=driver,author = author_name,rating=rating,comment=comment)
            fback.save()
        except ride_request.DoesNotExist:
            print "in the ride_request not exist exception"
            return HttpResponse(json.dumps({'errCode':ERR_NO_RIDER_DRIVER_CONTACT}),content_type="application/json")
                
                
    except KeyError:
        return HttpResponse(json.dumps({'errCode':ERR_DATABASE_SEARCH_ERROR}),content_type="application/json")
    
    return HttpResponse(json.dumps({'errCode':SUCCESS}),content_type="application/json")







