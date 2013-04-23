"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import unittest
import StringIO
import json
import testLib
import testUtils
import os
from datetime import date, datetime, time, timedelta
from django.test.client import Client
from carpoolapp.unitTest import *
import views
import models
import unittest


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


class TestUnit(testLib.RestTestCase):


    """Issue a REST API request to run the unit tests, and analyze the result"""
    def testUnit(self):
        buffer = StringIO.StringIO()
        suite = unittest.TestLoader().loadTestsFromTestCase(UnitTest)
        result = unittest.TextTestRunner(stream = buffer, verbosity = 2).run(suite)
        rv = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": buffer.getvalue()}
        self.assertTrue('output' in rv)
        print ("Unit tests output:\n"+
               "\n***** ".join(rv['output'].split("\n")))
        self.assertTrue('totalTests' in rv)
        print "***** Reported "+str(rv['totalTests'])+" unit tests"
        # When we test the actual project, we require at least 40 unit tests
        minimumTests = 40
        if "SAMPLE_APP" in os.environ:
            minimumTests = 4
        self.assertTrue(rv['totalTests'] >= minimumTests,
                        "at least "+str(minimumTests)+" unit tests. Found only "+str(rv['totalTests'])+". use SAMPLE_APP=1 if this is the sample app")
        self.assertEquals(0, rv['nrFailed'])

class SignupTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)
    #checks that standard input for setting up a rider works
    def testSignupRider1(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@yahoo.com', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0} )
        print("testSignupRider1")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.SUCCESS)

    #checks that standard input for setting up a rider works with strange naming 

    def testSignupRider2(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'Symb!@#$%^&*', 'lastname' : 'Symb!@#$%^&*', 'email' : 'alex.christ@be.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0} )
        print("testSignupRider2")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.SUCCESS)

    #checks that standard input for setting up a rider fails with long names 
    def testSignupRider3(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'Longfirstnameiswayyyyywayyyytoolong', 'lastname' : 'Cihla', 'email' : 'alex.pena@bs2.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0} )
        print("testSignupRider3")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a rider fails with long names 
    def testSignupRider4(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Longlastnameiswayyyyywayyyytoolong', 'email' : 'alex.doumbe@bs3.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0} )
        print("testSignupRider4")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a rider fails with bad -email format
    def testSignupRider6(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password','email':'aime.com', 'cellphone' : '408-826-9366', 'driver' : 0} )
        print("testSignupRider6")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_EMAIL)
    #cheks that standard input for for setting up a rider fails with non-email
    def testSignupRidernoemail(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'email':'','cellphone' : '408-826-9366', 'driver' : 0} )
        print("testSignupRidernoemail")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_EMAIL)
    #
    #checks that standard input for setting up a rider fails with non-date format dob
    def testSignupRider7(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.panick@bs5.edu', 'dob' : '03-23-423553', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0} )
        print("testSignupRider7")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a rider fails with long password
    def testSignupRider8(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.tenkeu@bs6.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'passwordiswayyyywayyyywayyytoolong', 'cellphone' : '408-826-9366', 'driver' : 0} )
        print("testSignupRider8")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #checks that standard input for setting up a rider works with different cellphone number formats
    def testSignupRider9(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.peter@bs7.com', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '(408)8269366', 'driver' : 0} )
        print("testSignupRider9")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #checks that standard input for setting up a rider works with different cellphone number formats
    def testSignupRider10(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.ciron@bs8.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0} )
        print("testSignupRider10")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.SUCCESS)
    
    #checks that standard input for setting up a rider fails with improperly formatted number
    def testSignupRider11(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.anita@bs10.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-93668', 'driver' : 0} )
        print("testSignupRider11")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a rider fails because email already in use
    
    def testSignupRider12(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@yahoo.com', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0} )
        print("testSignupRider12")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_USER_EXISTS)
    


    #checks that standard input for setting up a driver works 
    def testSignupDriver1(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.gatech@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2} )
        print("testSignupDriver1")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.SUCCESS)

    #sign up with expired email
    def test_ExpiredLicense(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'Aime', 'lastname' : 'Ngongang', 'email' : 'marianikgatech@berkeley.edu', 'dob' : '04-17-1950', 'sex' : 'male', 'password' : 'password', 'cellphone' : '510-459-3078', 'driver' : 1, 'license_no' : 'abcdefghij', 'license_exp' : '03-12-2008', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2} )
        print("testExpiredLicense")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_EXPIRED_LICENSE)
    

    #checks that standard input for setting up a driver fails with long license number 
    def testSignupDriver2(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.purdue@bs12.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sfesuperrrrrrrrrrdupperrrrrrrrrrrrrrlongggggggggggggggggggggggggggasdfghjasdfghjk', 'license_exp' : '03-12-2016', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2} )
        print("testSignupDriver2")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    
    #checks that standard input for setting up a driver fails with wrong format for exp date 
    def testSignupDriver3(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.chicago@bs13.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '02342322017', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2} )
        print("testSignupDriver3")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    
    #checks that standard input for setting up a driver fails with long car make field
    def testSignupDriver4(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.guiness@bs14.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '02-03-2018', 'car_make' : 'Honda Accord LONGCRAPLONGCRAPLONGCRAP', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2} )
        print("testSignupDriver4")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a driver fails with long car type field
    def testSignupDriver5(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.putain@bs15.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '02-03-2019', 'car_make' : 'Honda Accord', 'car_type' : 'SedanLONGLONGLONGLONGCRAPPPPPP', 'car_mileage' : 30, 'max_passengers' : 2} )
        print("testSignupDriver5")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a driver fails with wrong mileage field
    def testSignupDriver6(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.adal@bs16.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '02-03-2014', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : '3034', 'max_passengers' : 2} )
        print("testSignupDriver6")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a driver fails with wrong max passenger field
    def testSignupDriver7(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.bianca@bs17.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '02-03-2020', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : '2453'} )
        print("testSignupDriver7")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #check good iput
    def testSignup1(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.larissa@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':0})
        print("signupTest1")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.SUCCESS)
    #check too long firstname 
    def testSignup2(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJAJAJAJAJAJAJAJAJAJAJAJAJAJAAJAJAJAJAJAJAJAJA','lastname':'Cihla','email':'alex.corine@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':0})
        print("signupTest2")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check too long lastname
    def testSignup3(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihlacihlacihlacihlacihlacihlacihlacihlacihla','email':'alex.donald@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':0})
        print("signupTest3")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check invalid email 
    """def testSignup4(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihlayahoocom','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':0})
        print("signupTest1")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_EMAIL) """
    #check invalid date type 
    def testSignup5(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.bibi@yahoo.com','dob':'04311992','sex':'male','password':'password','cellphone':'510-459-3078','driver':0})
        print("signupTest5")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check invalid SEX 
    def testSignup6(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.evarist@yahoo.com','dob':'04-17-1992','sex':'garcon','password':'password','cellphone':'510-459-3078','driver':0})
        print("signupTest6")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check too long password
    def testSignup7(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.monfrere@yahoo.com','dob':'04-17-1992','sex':'male','password':'passwordpasswordpasswordpasswordpasswordpasswordpasswordpassword','cellphone':'510-459-3078','driver':0})
        print("signupTest7")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check invalid driver type
    def testSignup9(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.masoeur@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':'vrai'})
        print("signupTest9")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    # check valid driver info
    def testSignup10(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.parents@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':1,'license_no':'blahblahblaha','license_exp':'05-15-2017','car_make':'mercedes_benz','car_type':'sedan','car_mileage':100000,'max_passengers':2})
        print("signupTest10")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.SUCCESS)
    #check too long license_no
    def testSignup11(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.etoo@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':1,'license_no':'blahblahblahablahblahblahblahblahblahblahblahblah','license_exp':'05-15-2017','car_make':'mercedes_benz','car_type':'sedan','car_mileage':100000,'max_passengers':2})
        print("signupTest11")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check no car_make
    def testSignup12(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.samuel@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':1,'license_no':'blahblahbla','license_exp':'05-15-2017','car_make':'','car_type':'sedan','car_mileage':100000,'max_passengers':2})
        print("signupTest12")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check null car_type
    def testSignup13(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.song@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':1,'license_no':'blahblah','license_exp':'05-15-2017','car_make':'mercedes_benz','car_type':'','car_mileage':100000,'max_passengers':2})
        print("signupTest13")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check invalid expiration date
    def testSignup14(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.alex@yahoo.com','dob':'04171992','sex':'male','password':'password','cellphone':'510-459-3078','driver':1,'license_no':'blahblah','license_exp':'05152017','car_make':'mercedes_benz','car_type':'','car_mileage':100000,'max_passengers':2})
        print("signupTest14")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check invalid mileage type
    def testSignup15(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.makoun@yahoo.com','dob':'04171992','sex':'male','password':'password','cellphone':'510-459-3078','driver':1,'license_no':'blahblah','license_exp':'05-15-2017','car_make':'mercedes_benz','car_type':'suv','car_mileage':'aaaaa','max_passengers':2})
        print("signupTest15")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check invalid maxpassenger type
    def testSignup16(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.jean@yahoo.com','dob':'04171992','sex':'male','password':'password','cellphone':'510-459-3078','driver':1,'license_no':'blahblah','license_exp':'05-15-2017','car_make':'mercedes_benz','car_type':'suv','car_mileage':100000,'max_passengers':'aaaaa'})
        print("signupTest16")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

class LoginTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        expected = { 'errCode' : errCode }
        self.assertDictEqual(expected, respData)
    #check we have good input
    def testZLogin1(self):
        respData = self.makeRequest("/login",method="POST",data = {'email' :'alex.cihla@yahoo.com','password':'password'})
        print("testLogin1")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.SUCCESS)
    #check invalid iput with no  email
    def testzLogin2(self):
        respData = self.makeRequest("/login",method="POST",data = {'email':'','password':'password'})
        print("testLogin2")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_EMAIL)
    #check very long passwordi
    def testzLogin3(self):
        respData = self.makeRequest("/login",method="POST",data = {'email' :'alex.chila@berkeley.edu','password':'passwordpasswordpasswordpasswordpasswordpassword'})
        print("testLogin3")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #check we have a wrong match
    def testzLogin4(self):
        respData = self.makeRequest("/login",method="POST",data = {'email' :'douala@mbanga.yaounde','password':'password'})
        print("testLogin4")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_NOT_USER)
    #check user exist
    def testzLogin5(self):
        respData = self.makeRequest("/login",method="POST",data = {'email' :'alex.chila@berkeley.edu','password':'doualacameroun'})
        print("testLogin5")
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.ERR_NOT_USER) 




class ZAddRouteTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

    #generic first add route test with legitimate coordinates
    def testzAddGood1(self):
        testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {}) #User.objects.get(email = "alex.gatech@berkeley.edu").apikey
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi["apikey"],"edt":"0:36","dest-lat":"37.83421105081068","depart-long":"-122.27687716484068","depart-lat":"37.856989109666834","date":"04-09-2013","dest-long":"-122.27281998842956"} )
        print("testAddGood1")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)
    """
    def testAddGoodUnit1(self):
        testDriver = testUtils.genDriver()
        driverApi = testDriver.driver.apikey
        data = { 'apikey' : 'f2b8b1a60723c5763422d6d5ba25a0594ee2cecc',"edt":"0:36","dest-lat":"37.83421105081068","depart-long":"-122.27687716484068","depart-lat":"37.856989109666834","date":"04-09-2013","dest-long":"-122.27281998842956"}
        request =  = json.loads('data' : { 'apikey' : 'f2b8b1a60723c5763422d6d5ba25a0594ee2cecc',"edt":"0:36","dest-lat":"37.83421105081068","depart-long":"-122.27687716484068","depart-lat":"37.856989109666834","date":"04-09-2013","dest-long":"-122.27281998842956"} )
        response = views.addroute(request)
        self.assertResponse(response, testLib.RestTestCase.SUCCESS)

    """
    def testzAddGood2(self):
        testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi["apikey"],"edt":"23:36","dest-lat":"37.83421105081068","depart-long":"-122.27687716484068","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddGood2")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testzAddGood3(self):
        testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi["apikey"],"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-122.27687716484068","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-172.27281998842956"} )
        print("testAddGood3")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testzAddGood4(self):
        testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi["apikey"],"edt":"2:36","dest-lat":"87.83421105081068","depart-long":"-172.27687716484068","depart-lat":"85.856989109666834","date":"04-17-2013","dest-long":"-128.27281998842956"} )
        print("testAddGood4")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    #checks that coordinates on departure are good
    def testzAddBadDep5(self):
        testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi["apikey"],"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-192.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadDep5")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    def testzAddBadDep6(self):
        testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi["apikey"],"edt":"2:36","dest-lat":"67.83421105081068","depart-long":"-162.080078","depart-lat":"97.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadDep6")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    def testzAddBadDep7(self):
        testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi["apikey"],"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"192.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadDep8")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    def testzAddBadDep8(self):
        testApi = (User.objects.get(email = 'alex.gatech@berkeley.edu')).apikey
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi["apikey"],"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-132.080078","depart-lat":"-91.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadDep8")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    #checks that coordinates on destination are good
    def testzAddBadDest9(self):
        testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi["apikey"],"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-142.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-182.27281998842956"} )
        print("testAddBadDest9")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    def testzAddBadDest10(self):
        testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi["apikey"],"edt":"2:36","dest-lat":"97.83421105081068","depart-long":"-162.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadDest10")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    def testzAddBadDest11(self):
        testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi["apikey"],"edt":"2:36","dest-lat":"97.83421105081068","depart-long":"-122.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"132.27281998842956"} )
        print("testAddBadDest11")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    def testzAddBadDest12(self):
        testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi["apikey"],"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-133.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"192.27281998842956"} )
        print("testAddBadDest12")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    #to check that adding route only works for established drivers
    def testzAddGoodUser13(self):
        testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi["apikey"],"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-132.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddGoodUser13")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testzAddBadUser14(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : '27d006284191d231b9639018d9bcf6947641',"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-162.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadUser14")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_APIKEY)

    def testzAddBadUser15(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : '27d006284191d231b9639d18d9bcf6947641',"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-12.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadUser15")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_APIKEY)

    def testzAddBadUser16(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : '27d006284191d23190bc9d18d9bcf6947641',"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-122.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadUser16")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_APIKEY)
        

class ZSearchTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

    
    def testzSearch1(self):
        print "testSearch1"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.SUCCESS)

    def testzSearch2(self):
        print "testSearch2"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) >= 0)
        self.assertEquals(t, True)

    def testzSearch3(self):
        print "testSearch3"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) > 0)
        if t:
            rides = respData.get("rides", None)
            self.assertTrue(rides != None);
            for ride in rides:
                status = ride.get("status", None)
                self.assertEquals(status, "valid")

    def testzSearch4(self):
        print "testSearch4"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) > 0)
        if t:
            rides = respData.get("rides", None)
            self.assertTrue(rides != None);
            for ride in rides:
                driver_info = ride.get("driver_info", None)
                self.assertTrue(driver_info != None)

    def testzSearch5(self):
        print "testSearch5"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) > 0)
        if t:
            rides = respData.get("rides", None)
            self.assertTrue(rides != None);
            for ride in rides:
                driver_info = ride.get("driver_info", None)
                self.assertTrue(driver_info != None)
                driver = driver_info.get("driver", None)
                self.assertTrue(driver != None)

class ZManageRouteTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testzzManageRoute1(self):
        print "testManageRoute1"
        respData = self.makeRequest("/driver/manageRoute", method="GET", data = { 'apikey' : '06284191d231b96390bc9d18d9bcf6947641'} )
        self.assertTrue(respData.get("errCode",-1) == testLib.RestTestCase.SUCCESS)

    def testzzManageRoute2(self):
        print "testManageRoute2"
        respData = self.makeRequest("/driver/manageRoute", method="GET", data = { 'apikey' : '27d00231b96390bc9d18d9bcf6947641'} )
        self.assertTrue(respData.get("errCode",-1) == testLib.RestTestCase.ERR_BAD_APIKEY)

    def testzzManageRoute3(self):
        print "testManageRoute3"
        respData = self.makeRequest("/driver/manageRoute", method="GET", data = { 'apikey' : '28b1f28813b70771cc26838e40fe9199167b4c76'} )
        self.assertTrue(respData.get("errCode",-1) == testLib.RestTestCase.ERR_BAD_DRIVER_INFO)

"""class RiderStatusTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

    
    def testUserPendingRides(self):
        print "testUserPendingRides"
        self.makeRequest("/rider/select",method="POST",data={'rider_id':1,'route_id':20,'comment':"I would like a ride from you"})
        self.makeRequest("/rider/select",method="POST",data={'rider_id':1,'route_id':60,'comment':"I would like a ride from you"})
        
        expected_dict = {}
        expected_dict[20]={'driver_firstname':"Peter",
        'driver_lastname':"Lee",
        'route_depart_lat':"27.50233",
        'route_depart_lg':"-142.080078",
        'route_arrive_lat':"-37.509413",
        'route_arrive_lg':"-12.000078",
        'departure_time':"2013-04-06 19:16:14.689763+00:00",
        'comment':"I would like a ride from you"}
        expected_dict[60]={'driver_firstname':"Peter",
        'driver_lastname':"Lee",
        'route_depart_lat':"27.50233",
        'route_depart_lg':"-142.080078",
        'route_arrive_lat':"-37.509413",
        'route_arrive_lg':"-12.000078",
        'departure_time':"2013-04-08 04:35:21.223602+00:00",
        'comment':"I would like a ride from you"}
        
        respData = self.makeRequest("/rides/pending", method="POST", data = { 'rider_id':1} )
        self.assertEquals(respData, expected_dict.values())

    def testUserDeniedRides(self):
   
        print "testUserDeniedRides "
        self.makeRequest("/driver/accept?from=1&to=1&route_id=20&response=0", method="GET")
   
        self.makeRequest("/driver/accept?from=1&to=1&route_id=60&response=0", method="GET")
        
        expected_dict = {}
        expected_dict[20]={'driver_firstname':"Peter",
        'driver_lastname':"Lee",
        'route_depart_lat':"27.50233",
        'route_depart_lg':"-142.080078",
        'route_arrive_lat':"-37.509413",
        'route_arrive_lg':"-12.000078",
        'departure_time':"2013-04-06 19:16:14.689763+00:00",
        'comment':"I would like a ride from you"}
        expected_dict[60]={'driver_firstname':"Peter",
        'driver_lastname':"Lee",
        'route_depart_lat':"27.50233",
        'route_depart_lg':"-142.080078",
        'route_arrive_lat':"-37.509413",
        'route_arrive_lg':"-12.000078",
        'departure_time':"2013-04-08 04:35:21.223602+00:00",
        'comment':"I would like a ride from you"}
        
        respData = self.makeRequest("/rides/denied", method="POST", data = { 'rider_id':3} )
        self.assertEquals(respData, expected_dict.values())
    
    def testUserCanceledRides(self):
        print "testUserPendingRides"
        self.makeRequest("/cancel/ride",method="POST",data={'rider_id':1,'route_id':20,'comment':"Sorry I changed my mind"})
        self.makeRequest("/cancel/ride",method="POST",data={'rider_id':1,'route_id':60,'comment':"sorry i changed my mind"})
        
        expected_dict = {}
        expected_dict[20]={'driver_firstname':"Peter",
        'driver_lastname':"Lee",
        'route_depart_lat':"27.50233",
        'route_depart_lg':"-142.080078",
        'route_arrive_lat':"-37.509413",
        'route_arrive_lg':"-12.000078",
        'departure_time':"2013-04-06 19:16:14.689763+00:00",
        'comment':"sorry i changed my mind"}
        expected_dict[60]={'driver_firstname':"Peter",
        'driver_lastname':"Lee",
        'route_depart_lat':"27.50233",
        'route_depart_lg':"-142.080078",
        'route_arrive_lat':"-37.509413",
        'route_arrive_lg':"-12.000078",
        'departure_time':"2013-04-08 04:35:21.223602+00:00",
        'comment':"sorry i changed my mind"}
        
        respData = self.makeRequest("/rides/canceled", method="POST", data = { 'rider_id':1} )
        self.assertEquals(respData, expected_dict.values())
    
    def testUserAcceptedRides(self):
        print "testUserPendingRides"
        self.makeRequest("/driver/accept?from=1&to=1&route_id=20&response=1", method="GET")
   
        self.makeRequest("/driver/accept?from=1&to=1&route_id=60&response=1", method="GET")
        

        expected_dict = {}
        expected_dict[20]={'driver_firstname':"Peter",
        'driver_lastname':"Lee",
        'route_depart_lat':"27.50233",
        'route_depart_lg':"-142.080078",
        'route_arrive_lat':"-37.509413",
        'route_arrive_lg':"-12.000078",
        'departure_time':"2013-04-06 19:16:14.689763+00:00",
        'comment':"I would like a ride from you"}
        expected_dict[60]={'driver_firstname':"Peter",
        'driver_lastname':"Lee",
        'route_depart_lat':"27.50233",
        'route_depart_lg':"-142.080078",
        'route_arrive_lat':"-37.509413",
        'route_arrive_lg':"-12.000078",
        'departure_time':"2013-04-08 04:35:21.223602+00:00",
        'comment':"I would like a ride from you"}
        
        respData = self.makeRequest("/rides/accepted", method="POST", data = { 'rider_id':1} )
        self.assertEquals(respData, expected_dict.values())


class Select_RideTest(testLib.RestTestCase):
  def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

  def testSelect_Good_Ride(self):
    respData = self.makeRequest("/rider/select", method="POST", data = { 'rider_id' : 3, 'route_id' : 50,'comment':''} )
    print("testSelect_Good_Ride")
    self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

  def testSelect_BAD_Ride(self):
    respData = self.makeRequest("/rider/select", method="POST", data = { 'rider_id' : 1, 'route_id' : 2000,'comment':''} )
    print("testSelect_BAD_Ride")
    self.assertResponse(respData, testLib.RestTestCase.ERR_DATABASE_SEARCH_ERROR)

class Accept_OR_Deny_RideTest(testLib.RestTestCase):
  def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)
  
  def test_Accept_Good_Ride(self):
    respData = self.makeRequest("/driver/accept?from=3&to=1&route_id=50&response=1", method="GET")
    print("test_Accept_Good_Ride")
    self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

  def test_Accept_BAD_Ride(self):
    respData = self.makeRequest("/driver/accept?from=-1&to=-10&route_id=0&response=0", method="GET")
    print("test_Accept_BAD_Ride")
    self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_SERVER_RESPONSE)
  """
