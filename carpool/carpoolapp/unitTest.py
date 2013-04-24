from django.test import TestCase
from django.utils import unittest
import json
import testLib
import testUtils
import os
from datetime import date, datetime, time, timedelta
from django.test.client import Client
import views
import models


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
MAX_LENGTH_FIRST_LAST_PASS = 15 #max length for first and last name and password
MAX_LENGTH_EMAIL = 50  #max length email
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

class UnitTest(unittest.TestCase):
        """
        Unittests for the Users model class (a sample, incomplete)
        """
        def setUp(self):
            os.environ['DJANGO_SETTINGS_MODULE'] = "mysite.settings"
            testUtils.genDriver()
            testUtils.genDriver()
            testUtils.genUser()
            testUtils.genUser()
            self.users = models.User()
            self.routes = models.Route()


        #
        # SIGNUP USER AND DRIVER!
        #

        #successful addition of a user
        def testAddUser1(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@yahoo.com', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))

        #successful addition of a user
        def testAddUser2(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'Symb!@#$%^&*', 'lastname' : 'Symb!@#$%^&*', 'email' : 'alex.christ@be.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))

        #long firstname
        def testAddUser3(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'Longfirstnameiswayyyyywayyyytoolong', 'lastname' : 'Cihla', 'email' : 'alex.pena@bs2.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #long lastname
        def testAddUser4(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Longlastnameiswayyyyywayyyytoolong', 'email' : 'alex.doumbe@bs3.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #bad email
        def testAddUser5(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password','email':'aime.com', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_EMAIL, response.get("errCode"))

        #bad email
        def testAddUser6(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password','email':'yahoo.com', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_EMAIL, response.get("errCode"))

        #bad email
        def testAddUser7(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password','email':'', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_EMAIL, response.get("errCode"))

        #bad dob
        def testAddUser8(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.panick@bs5.edu', 'dob' : '03-23-423553', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #password too long
        def testAddUser9(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.tenkeu@bs6.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'passwordiswayyyywayyyywayyytoolong', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #cell phone formatted incorrectly
        def testAddUser10(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.peter@bs7.com', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '(408)8269366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #cell number too long
        def testAddUser11(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.anita@bs10.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-93668', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #all good here... rechecking with different info
        def testAddUser12(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'Alexander', 'lastname' : 'JamesCihla', 'email' : 'alex.ciron@bs8.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))

        #bad sex type
        def testAddUser13(self):
            newrequest = views.request
            newrequest.body = json.dumps({'firstname':'AJ','lastname':'Cihla','email':'alex.evarist@yahoo.com','dob':'04-17-1992','sex':'garcon','password':'password','cellphone':'510-459-3078','driver':0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #invalid driver type
        def testAddUser14(self):
            newrequest = views.request
            newrequest.body = json.dumps({'firstname':'AJ','lastname':'Cihla','email':'alex.masoeur@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':'vrai'})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))


        #no car make
        def testAddUser15(self):
            newrequest = views.request
            newrequest.body = json.dumps({'firstname':'AJ','lastname':'Cihla','email':'alex.samuel@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':1,'license_no':'blahblahbla','license_exp':'05-15-2017','car_make':'','car_type':'sedan','car_mileage':100000,'max_passengers':2})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #null car type
        def testAddUser16(self):
            newrequest = views.request
            newrequest.body = json.dumps({'firstname':'AJ','lastname':'Cihla','email':'alex.song@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':1,'license_no':'blahblah','license_exp':'05-15-2017','car_make':'mercedes_benz','car_type':'','car_mileage':100000,'max_passengers':2})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #bad experation date
        def testAddUser17(self):
            newrequest = views.request
            newrequest.body = json.dumps({'firstname':'AJ','lastname':'Cihla','email':'alex.alex@yahoo.com','dob':'04171992','sex':'male','password':'password','cellphone':'510-459-3078','driver':1,'license_no':'blahblah','license_exp':'05152017','car_make':'mercedes_benz','car_type':'','car_mileage':100000,'max_passengers':2})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))



        #
        #SIGNUP DRIVER
        #
        #successful addition
        def testAddDriver1(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.gatech@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))

        #license is old
        def testAddDriver2(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'Aime', 'lastname' : 'Ngongang', 'email' : 'marianikgatech@berkeley.edu', 'dob' : '04-17-1950', 'sex' : 'male', 'password' : 'password', 'cellphone' : '510-459-3078', 'driver' : 1, 'license_no' : 'abcdefghij', 'license_exp' : '03-12-2008', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2} )
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_EXPIRED_LICENSE, response.get("errCode"))

        #license number is too long/weird
        def testAddDriver3(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.purdue@bs12.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sfesuperrrrrrrrrrdupperrrrrrrrrrrrrrlongggggggggggggggggggggggggggasdfghjasdfghjk', 'license_exp' : '03-12-2016', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2} )
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #wrong date format for exp date
        def testAddDriver4(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.chicago@bs13.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '02342322017', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2} )
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #bad/extra long car make field
        def testAddDriver5(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.guiness@bs14.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '02-03-2018', 'car_make' : 'Honda Accord LONGCRAPLONGCRAPLONGCRAP', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2} )
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #bad/extra long car type field
        def testAddDriver6(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.putain@bs15.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '02-03-2019', 'car_make' : 'Honda Accord', 'car_type' : 'SedanLONGLONGLONGLONGCRAPPPPPP', 'car_mileage' : 30, 'max_passengers' : 2} )
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #bad mileage entry
        def testAddDriver7(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.adal@bs16.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '02-03-2014', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : '3034', 'max_passengers' : 2} )
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #bad max passenger field
        def testAddDriver8(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.bianca@bs17.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '02-03-2020', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : '2453'} )
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))


        #
        #CHECK LOGGING IN
        #
        #clean login
        def testLoginUser1(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.unique@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2})
            views.signup(newrequest)
            newrequest.body = json.dumps({'email':'alex.unique@berkeley.edu', 'password':'password'})
            response = views.login(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))

        #clean login
        def testLoginUser2(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.gatech@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2})
            views.signup(newrequest)
            newrequest.body = json.dumps({'email':'','password':'password'})
            response = views.login(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_EMAIL, response.get("errCode"))

        #clean login
        def testLoginUser3(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.gatech@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2})
            views.signup(newrequest)
            newrequest.body = json.dumps({'email' :'alex.chila@berkeley.edu','password':'passwordpasswordpasswordpasswordpasswordpassword'})
            response = views.login(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #clean login
        def testLoginUser4(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.gatech@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2})
            views.signup(newrequest)
            newrequest.body = json.dumps({'email' :'douala@mbanga.yaounde','password':'password'})
            response = views.login(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_NOT_USER, response.get("errCode"))

        #clean login
        def testLoginUser5(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.gatech@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2})
            views.signup(newrequest)
            newrequest.body = json.dumps({'email' :'alex.gatech@berkeley.edu','password':'doualacameroun'})
            response = views.login(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_NOT_USER, response.get("errCode"))




        #
        #TESTING ADDING ROUTES
        #

        #clean route addition
        def testAddRoute1(self):
            newrequest = views.request
            testDriver = testUtils.genDriver()
            testApi = testDriver.driver.apikey
            newrequest.body = json.dumps({ 'apikey' : testApi,"edt":"0:36","dest-lat":"37.83421105081068","depart-long":"-122.27687716484068","depart-lat":"37.856989109666834","date":"04-09-2013","dest-long":"-122.27281998842956"} )
            response = views.addroute(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))



            
        #
        #CHECK SANITIZATION EFFORTS
        #

        #checking that destination coordinates received from front end are legit and will be mappable if neccessary
        def testUnitHandleRouteDataCleaner1(self):
            #Tests that adding a user works
            self.assertEquals(testLib.RestTestCase.SUCCESS, views.handleRouteData(1, "-122.080078", "37.279413","-122.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner2(self):
            #Tests that adding a route fails with bad destination location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DESTINATION , views.handleRouteData(1, "-122.080078", "37.279413","-122.088878", "98.579413"))

        def testUnitHandleRouteDataCleaner3(self):
            #Tests that adding a route fails with bad destination location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DESTINATION, views.handleRouteData(1, "-122.080078", "37.279413","182.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner4(self):
            #Tests that adding a route fails with bad destination location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DESTINATION, views.handleRouteData(1, "-122.080078", "37.279413","-122.088878", "97.579413"))

        def testUnitHandleRouteDataCleaner5(self):
            #Tests that adding a route fails with bad destination location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DESTINATION, views.handleRouteData(1, "-122.080078", "37.279413","-192.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner6(self):
            #Tests that adding a route fails with bad destination location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DESTINATION, views.handleRouteData(1, "-122.080078", "37.279413","-122.088878", "97.523322223479413"))

        def testUnitHandleRouteDataCleaner7(self):
            #Tests that adding a route fails with bad destination location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DESTINATION, views.handleRouteData(1, "-122.080078", "37.279413","-182.08823434223878", "37.579413"))

        #checking that departure coordinates received from front end are legit and will be mappable if neccessary
        def testUnitHandleRouteDataCleaner8(self):
            #Tests that adding a route fails with bad departure location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DEPARTURE, views.handleRouteData(1, "-190.080078", "37.279413","-122.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner9(self):
            #Tests that adding a route fails with bad departure location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DEPARTURE, views.handleRouteData(1, "-122.080078", "91.279413","-122.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner10(self):
            #Tests that adding a route fails with bad departure location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DEPARTURE, views.handleRouteData(1, "192.080078", "37.279413","-132.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner11(self):
            #Tests that adding a route fails with bad departure location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DEPARTURE, views.handleRouteData(1, "-122.080078", "-137.279413","-122.088878", "65.579413"))

        def testUnitHandleRouteDataCleaner12(self):
            #Tests that adding a route fails with bad departure location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DEPARTURE, views.handleRouteData(1, "-192.082333234320078", "37.279413","-122.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner13(self):
            #Tests that adding a route fails with bad departure location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DEPARTURE, views.handleRouteData(1, "-122.0823378", "91.272349234234413","-122.088878", "37.579413"))

        #checking with different BAD userid numbers... they should always fail ASSUMING THAT WE DONT CREATE MORE THAN 999999999 users
        def testUnitHandleRouteDataCleaner14(self):
            #Tests that adding a route with bad userid fails
            self.assertEquals(testLib.RestTestCase.ERR_BAD_USERID, views.handleRouteData(-233, "-122.080078", "37.279413","-122.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner15(self):
            #Tests that adding a route with bad userid fails
            self.assertEquals(testLib.RestTestCase.ERR_BAD_USERID, views.handleRouteData(99999999, "-122.080078", "37.279413","-122.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner16(self):
            #Tests that adding a route with bad userid fails
            self.assertEquals(testLib.RestTestCase.ERR_BAD_USERID, views.handleRouteData(-1, "-122.080078", "37.279413","-122.088878", "37.579413"))

        def testUnitModelUserToDict(self):
            #Test if to_dict method works properly
            users = models.User.objects.all()
            if len(users) > 0:
                user = users[0]
                dic = user.to_dict()
                fields = ["firstname", "lastname", "email", "dob", "sex", "cellphone", "user_type", "comments", "avg_rating"]
                for field in fields:
                    self.assertEquals(dic.get(field,None), eval("user."+field))

        def testUnitModelUserToDictUnsecure(self):
            #Test if to_dict method works properly
            users = models.User.objects.all()
            if len(users) > 0:
                user = users[0]
                dic = user.to_dict_unsecure()
                fields = ["firstname", "lastname",  "email", "dob", "sex", "password", "cellphone", "user_type", "comments", "avg_rating"]
                for field in fields:
                    self.assertEquals(dic.get(field,None), eval("user."+field))

        def testUnitModelDriverInfoToDict(self):
            #Test if to_dict method works properly
            di = models.DriverInfo.objects.all()
            if len(di) > 0:
                di= di[0]
                dic = di.to_dict()
                fields = ["license_no", "license_exp", "car_make", "car_type", "car_mileage", "max_passengers"]
                for field in fields:
                    self.assertEquals(dic.get(field,None), eval("di."+field))

        def testUnitModelRouteToDict(self):
            #Test if to_dict method works properly
            routes = models.Route.objects.all()
            if len(routes) > 0:
                route= routes[0]
                dic = route.to_dict()
                fields = ["depart_time", "depart_lat", "depart_lg", "arrive_lat", "arrive_lg", "maps_info", "status"]
                for field in fields:
                    self.assertEquals(dic.get(field,None), eval("route."+field))

        
# If this file is invoked as a Python script, run the tests in this module
if __name__ == "__main__":
    # Add a verbose argument
    sys.argv = [sys.argv[0]] + ["-v"] + sys.argv[1:]
    unittest.main()