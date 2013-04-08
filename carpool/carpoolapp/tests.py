"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import json
import testLib
import os
from datetime import *

class TestUnit(testLib.RestTestCase):
    """Issue a REST API request to run the unit tests, and analyze the result"""
    def testUnit(self):
        respData = self.makeRequest("/TESTAPI/unitTests", method="POST")
        self.assertTrue('output' in respData)
        print ("Unit tests output:\n"+
               "\n***** ".join(respData['output'].split("\n")))
        self.assertTrue('totalTests' in respData)
        print "***** Reported "+str(respData['totalTests'])+" unit tests"
        # When we test the actual project, we require at least 40 unit tests
        minimumTests = 40
        if "SAMPLE_APP" in os.environ:
            minimumTests = 4
        self.assertTrue(respData['totalTests'] >= minimumTests,
                        "at least "+str(minimumTests)+" unit tests. Found only "+str(respData['totalTests'])+". use SAMPLE_APP=1 if this is the sample app")
        self.assertEquals(0, respData['nrFailed'])

class SignupTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)
    #checks that standard input for setting up a rider works
    def testSignupRider1(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@yahoo.com', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : False} )
        print("testSignupRider1")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    #checks that standard input for setting up a rider works with strange naming 

    def testSignupRider2(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'Symbolicname!@#$%^&*', 'lastname' : 'Symboliclast!@#$%^&*', 'email' : 'alex.cihla@bs1.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : False} )
        print("testSignupRider2")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    #checks that standard input for setting up a rider fails with long names 
    def testSignupRider3(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'Longfirstnameiswayyyyywayyyytoolong', 'lastname' : 'Cihla', 'email' : 'alex.cihla@bs2.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : False} )
        print("testSignupRider3")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a rider fails with long names 
    def testSignupRider4(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Longlastnameiswayyyyywayyyytoolong', 'email' : 'alex.cihla@bs3.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : False} )
        print("testSignupRider4")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a rider fails with non-email
    """def testSignupRider5(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla$berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : False} )
        print("testSignupRider5")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_EMAIL) """
    #checks that standard input for setting up a rider fails with non-email
    def testSignupRider6(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : False} )
        print("testSignupRider6")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_EMAIL)
    #checks that standard input for setting up a rider fails with non-date format dob
    def testSignupRider7(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@bs5.edu', 'dob' : '03-23-423553', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : False} )
        print("testSignupRider7")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a rider fails with long password
    def testSignupRider8(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@bs6.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'passwordiswayyyywayyyywayyytoolong', 'cellphone' : '408-826-9366', 'driver' : False} )
        print("testSignupRider8")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #checks that standard input for setting up a rider works with different cellphone number formats
    def testSignupRider9(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@bs7.com', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '(408)8269366', 'driver' : False} )
        print("testSignupRider9")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #checks that standard input for setting up a rider works with different cellphone number formats
    def testSignupRider10(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@bs8.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : False} )
        print("testSignupRider10")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)
    
    #checks that standard input for setting up a rider fails with improperly formatted number
    def testSignupRider11(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@bs10.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-93668', 'driver' : False} )
        print("testSignupRider11")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a rider fails because email already in use
    #def testSignupRider12(self):
     #   respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@yahoo.com', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : False} )
      #  print("testSignupRider12")
       # self.assertResponse(respData, testLib.RestTestCase.ERR_SOMETHING)



    #checks that standard input for setting up a driver works 
    def testSignupDriver1(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : True, 'license_no' : '20934089sfe', 'license_exp' : '03-12-2013', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : '30', 'max_passengers' : '2'} )
        print("testSignupDriver1")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    #checks that standard input for setting up a driver fails with long license number 
    def testSignupDriver1(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@bs12.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : True, 'license_no' : '20934089sfesuperrrrrrrrrrdupperrrrrrrrrrrrrrlongggggggggggggggggggggggggggasdfghjasdfghjk', 'license_exp' : '03-12-2013', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : '30', 'max_passengers' : '2'} )
        print("testSignupDriver2")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    
    #checks that standard input for setting up a driver fails with wrong format for exp date 
    def testSignupDriver3(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@bs13.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : True, 'license_no' : '20934089sf', 'license_exp' : '02342322013', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2} )
        print("testSignupDriver3")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    
    #checks that standard input for setting up a driver fails with long car make field
    def testSignupDriver4(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@bs14.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : True, 'license_no' : '20934089sf', 'license_exp' : '02-03-2013', 'car_make' : 'Honda Accord LONGCRAPLONGCRAPLONGCRAP', 'car_type' : 'Sedan', 'car_mileage' : '30', 'max_passengers' : '2'} )
        print("testSignupDriver4")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a driver fails with long car type field
    def testSignupDriver5(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@bs15.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : True, 'license_no' : '20934089sf', 'license_exp' : '02-03-2013', 'car_make' : 'Honda Accord', 'car_type' : 'SedanLONGLONGLONGLONGCRAPPPPPP', 'car_mileage' : '30', 'max_passengers' : '2'} )
        print("testSignupDriver5")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a driver fails with long mileage field
    def testSignupDriver6(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@bs16.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : True, 'license_no' : '20934089sf', 'license_exp' : '02-03-2013', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : '3034', 'max_passengers' : '2'} )
        print("testSignupDriver6")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a driver fails with long max passenger field
    def testSignupDriver7(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@bs17.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : True, 'license_no' : '20934089sf', 'license_exp' : '02-03-2013', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : '30', 'max_passengers' : '2453'} )
        print("testSignupDriver7")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #checks that standard input for setting up a driver fails because email is already in use 
    #def testSignupDriver8(self):
     #   respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@berkeley.edu', 'dob' : '04-17-1992', 'sex' : True, 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : True, 'license_no' : '20934089sfe', 'license_exp' : '03-12-2013', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : '30', 'max_passengers' : '2'} )
      #  print("testSignupDriver8")
       # self.assertResponse(respData, testLib.RestTestCase.ERR_SOMETHING)

    #check good iput
    def testSignup1(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihla@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':False})
        print("signupTest1")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)
    #check too long firstname 
    def testSignup2(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJAJAJAJAJAJAJAJAJAJAJAJAJAJAAJAJAJAJAJAJAJAJA','lastname':'Cihla','email':'alex.cihla@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':False})
        print("signupTest2")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check too long lastname
    def testSignup3(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihlacihlacihlacihlacihlacihlacihlacihlacihla','email':'alex.cihla@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':False})
        print("signupTest3")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check invalid email 
    """def testSignup4(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihlayahoocom','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':False})
        print("signupTest1")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_EMAIL) """
    #check invalid date type 
    def testSignup5(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihla@yahoo.com','dob':'04311992','sex':'male','password':'password','cellphone':'510-459-3078','driver':False})
        print("signupTest5")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check invalid SEX 
    def testSignup6(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihla@yahoo.com','dob':'04-17-1992','sex':'garcon','password':'password','cellphone':'510-459-3078','driver':False})
        print("signupTest6")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check too long password
    def testSignup7(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihla@yahoo.com','dob':'04-17-1992','sex':'male','password':'passwordpasswordpasswordpasswordpasswordpasswordpasswordpassword','cellphone':'510-459-3078','driver':False})
        print("signupTest7")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check invalid driver type
    def testSignup9(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihla@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':'vrai'})
        print("signupTest9")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    # check valid driver info
    def testSignup10(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihla@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':True,'license_no':'blahblahblaha','license_exp':'05-15-2017','car_make':'mercedes_benz','car_type':'sedan','car_mileage':100000,'max_passengers':2})
        print("signupTest10")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)
    #check too long license_no
    def testSignup11(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihla@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':True,'license_no':'blahblahblahablahblahblahblahblahblahblahblahblah','license_exp':'05-15-2017','car_make':'mercedes_benz','car_type':'sedan','car_mileage':100000,'max_passengers':2})
        print("signupTest11")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check no car_make
    def testSignup12(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihla@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':True,'license_no':'blahblahbla','license_exp':'05-15-2017','car_make':'','car_type':'sedan','car_mileage':100000,'max_passengers':2})
        print("signupTest12")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check null car_type
    def testSignup13(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihla@yahoo.com','dob':'04-17-1992','sex':'male','password':'password','cellphone':'510-459-3078','driver':True,'license_no':'blahblah','license_exp':'05-15-2017','car_make':'mercedes_benz','car_type':'','car_mileage':100000,'max_passengers':2})
        print("signupTest13")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check invalid expiration date
    def testSignup14(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihla@yahoo.com','dob':'04171992','sex':'male','password':'password','cellphone':'510-459-3078','driver':True,'license_no':'blahblah','license_exp':'05152017','car_make':'mercedes_benz','car_type':'','car_mileage':100000,'max_passengers':2})
        print("signupTest14")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check invalid mileage type
    def testSignup15(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihla@yahoo.com','dob':'04171992','sex':'male','password':'password','cellphone':'510-459-3078','driver':True,'license_no':'blahblah','license_exp':'05-15-2017','car_make':'mercedes_benz','car_type':'suv','car_mileage':'aaaaa','max_passengers':2})
        print("signupTest15")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)
    #check invalid maxpassenger type
    def testSignup16(self):
        respData = self.makeRequest("/signup",method ="POST",data ={'firstname':'AJ','lastname':'Cihla','email':'alex.cihla@yahoo.com','dob':'04171992','sex':'male','password':'password','cellphone':'510-459-3078','driver':True,'license_no':'blahblah','license_exp':'05-15-2017','car_make':'mercedes_benz','car_type':'suv','car_mileage':100000,'max_passengers':'aaaaa'})
        print("signupTest16")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

class LoginTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        expected = { 'errCode' : errCode }
        self.assertDictEqual(expected, respData)
    #check we have good input
    def testLogin1(self):
        respData = self.makeRequest("/login",method="POST",data = {'email' :'nadapeter@gmail.com','password':'asdf'})
        print("testLogin1")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)
    #check invalid iput with no  email
    def testLogin2(self):
        respData = self.makeRequest("/login",method="POST",data = {'email':'','password':'password'})
        print("testLogin2")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_EMAIL)
    #check very long passwordi
    def testLogin3(self):
        respData = self.makeRequest("/login",method="POST",data = {'email' :'alex.chila@berkeley.edu','password':'passwordpasswordpasswordpasswordpasswordpassword'})
        print("testLogin3")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH)

    #check we have a wrong match
    def testLogin4(self):
        respData = self.makeRequest("/login",method="POST",data = {'email' :'douala@mbanga.yaounde','password':'password'})
        print("testLogin4")
        self.assertResponse(respData, testLib.RestTestCase.ERR_NOT_USER)
    #check user exist
    def testLogin5(self):
        respData = self.makeRequest("/login",method="POST",data = {'email' :'alex.chila@berkeley.edu','password':'doualacameroun'})
        print("testLogin5")
        self.assertResponse(respData, testLib.RestTestCase.ERR_NOT_USER) 




class AddRouteTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

    #generic first add route test with legitimate coordinates
    def testAddGood1(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-122.080078', 'depart-lat' : '37.579413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413',"edt":str(datetime.now())} )
        print("testAddGood1")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)
    
    def testAddGood2(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-142.080078', 'depart-lat' : '27.50233', 'dest-long' : '-12.000078', 'dest-lat' : '-37.509413',"edt":str(datetime.now())} )
        print("testAddGood2")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testAddGood3(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'depart-long' : '-122.080078', 'depart-lat' : '-37.579413', 'dest-long' : '-122.000078', 'dest-lat' : '-37.509413', "edt":str(datetime.now())} )
        print("testAddGood3")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testAddGood4(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-122.080078', 'depart-lat' : '37.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413', "edt":str(datetime.now())} )
        print("testAddGood4")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    #checks that coordinates on departure are good
    def testAddBadDep5(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'depart-long' : '-192.080078', 'depart-lat' : '37.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413', "edt":str(datetime.now())} )
        print("testAddBadDep5")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    def testAddBadDep6(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-122.080078', 'depart-lat' : '100.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413', "edt":str(datetime.now())} )
        print("testAddBadDep6")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    def testAddBadDep7(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'depart-long' : '182.080078', 'depart-lat' : '97.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413', "edt":str(datetime.now())} )
        print("testAddBadDep8")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    def testAddBadDep8(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-192.080078', 'depart-lat' : '-92.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413', "edt":str(datetime.now())} )
        print("testAddBadDep8")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    #checks that coordinates on destination are good
    def testAddBadDest9(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'depart-long' : '-142.080078', 'depart-lat' : '37.579234413', 'dest-long' : '-182.000078', 'dest-lat' : '37.509413', "edt":str(datetime.now())} )
        print("testAddBadDest9")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    def testAddBadDest10(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-122.080078', 'depart-lat' : '60.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '97.509413', "edt":str(datetime.now())} )
        print("testAddBadDest10")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    def testAddBadDest11(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'depart-long' : '122.080078', 'depart-lat' : '47.579234413', 'dest-long' : '-192.000078', 'dest-lat' : '-97.509413', "edt":str(datetime.now())} )
        print("testAddBadDest11")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    def testAddBadDest12(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-132.080078', 'depart-lat' : '-12.579234413', 'dest-long' : '182.000078', 'dest-lat' : '137.509413', "edt":str(datetime.now())} )
        print("testAddBadDest12")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    #to check that adding route only works for established drivers
    def testAddGoodUser13(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'depart-long' : '-142.080078', 'depart-lat' : '37.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413', "edt":str(datetime.now())} )
        print("testAddGoodUser13")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testAddBadUser14(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : -1234, 'depart-long' : '-122.080078', 'depart-lat' : '60.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '17.509413', "edt":str(datetime.now())} )
        print("testAddBadUser14")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_USERID)

    def testAddBadUser15(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 99999999, 'depart-long' : '122.080078', 'depart-lat' : '47.579234413', 'dest-long' : '-132.000078', 'dest-lat' : '-37.509413', "edt":str(datetime.now())} )
        print("testAddBadUser15")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_USERID)

    def testAddBadUser16(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : -1, 'depart-long' : '-123.080078', 'depart-lat' : '-12.579234413', 'dest-long' : '132.000078', 'dest-lat' : '27.509413', "edt":str(datetime.now())} )
        print("testAddBadUser16")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_USERID)

class SearchTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

    
    def testSearch1(self):
        print "testSearch1"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.SUCCESS)

    def testSearch2(self):
        print "testSearch2"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) >= 0)
        self.assertEquals(t, True)

    def testSearch3(self):
        print "testSearch3"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) > 0)
        if t:
            rides = respData.get("rides", None)
            self.assertTrue(rides != None);
            for ride in rides:
                status = ride.get("status", None)
                self.assertEquals(status, "False")

    def testSearch4(self):
        print "testSearch4"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) > 0)
        if t:
            rides = respData.get("rides", None)
            self.assertTrue(rides != None);
            for ride in rides:
                driver_info = ride.get("driver_info", None)
                self.assertTrue(driver_info != None)

    def testSearch5(self):
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

        

class Select_RideTest(testLib.RestTestCase):
  def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

  def testSelect_Good_Ride(self):
    respData = self.makeRequest("/rider/select", method="POST", data = { 'rider_id' : 1, 'route_id' : 4} )
    print("testSelect_Good_Ride")
    self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

  def testSelect_BAD_Ride(self):
    respData = self.makeRequest("/rider/select", method="POST", data = { 'rider_id' : 1, 'route_id' : 2000} )
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
    respData = self.makeRequest("/driver/accept?route_id=1&response=1", method="GET")
    print("test_Accept_Good_Ride")
    self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

  def test_Accept_BAD_Ride(self):
    respData = self.makeRequest("/driver/accept?route_id=-1&response=1", method="GET")
    print("test_Accept_BAD_Ride")
    self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_SERVER_RESPONSE)

