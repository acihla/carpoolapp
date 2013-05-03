

   
	

from django.utils import unittest
import json
import testLib
import testUtils
from datetime import date, datetime, time, timedelta
import views
import models


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
ERR_UNKNOWN_DRIVER =-26
class UnitTest(unittest.TestCase):
        """
Unittests for the Users model class (a sample, incomplete)
"""
        '''
def setUp(self):
os.environ['DJANGO_SETTINGS_MODULE'] = "mysite.settings"
testUtils.genDriver()
testUtils.genDriver()
testUtils.genUser()
testUtils.genUser()
self.users = models.User()
self.routes = models.Route()

'''
        #
        # SIGNUP USER AND DRIVER!
        #

        #successful addition of a user
        def testAddUser1(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@yahoo.com', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print (response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))

        #successful addition of a user
        def testAddUser2(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'Symb!@#$%^&*', 'lastname' : 'Symb!@#$%^&*', 'email' : 'alex.christ@be.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print (response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))

        #long firstname
        def testAddUser3(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'Longfirstnameiswayyyyywayyyytoolong', 'lastname' : 'Cihla', 'email' : 'alex.pena@bs2.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            print(response)
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

        #cell phone formatted incorrectly but should still work
        def testAddUser10(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.peter@bs7.com', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '(408)8269366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))

        #cell number too long but should be parsed and saved
        def testAddUser11(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.anita@bs10.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-93668', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))

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
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.neverseen@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2})
            views.signup(newrequest)
            newrequest.body = json.dumps({'email':'alex.neverseen@berkeley.edu', 'password':'password'})
            response = views.login(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))

        #bad email
        def testLoginUser2(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.gatech@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2})
            views.signup(newrequest)
            newrequest.body = json.dumps({'email':'','password':'password'})
            response = views.login(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_EMAIL, response.get("errCode"))

        #bad password is too long
        def testLoginUser3(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.gatech@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2})
            views.signup(newrequest)
            newrequest.body = json.dumps({'email' :'alex.chila@berkeley.edu','password':'passwordpasswordpasswordpasswordpasswordpassword'})
            response = views.login(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #bad email
        def testLoginUser4(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.gatech@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2})
            views.signup(newrequest)
            newrequest.body = json.dumps({'email' :'douala@mbanga.yaounde','password':'password'})
            response = views.login(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_NOT_USER, response.get("errCode"))

        #bad password
        def testLoginUser5(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.gatech@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2})
            views.signup(newrequest)
            newrequest.body = json.dumps({'email' :'alex.gatech@berkeley.edu','password':'doualacameroun'})
            response = views.login(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_PASSWORD, response.get("errCode"))

        def testLoginUser6(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.gatech@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2})
            views.signup(newrequest)
            newrequest = json.dumps({'email' :'alex.gatech@berkeley.edu','password':'doualacameroun'})
            response = views.login(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_KEY, response.get("errCode"))


        #bad password
        def testLoginUser7(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.gatech@berkeley.edu', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2})
            views.signup(newrequest)
            newrequest.body = json.dumps({'email' :'alex.gatech@berkeley.eduthisshouldbewaywaywaytoooooooooooooooooooolonggggggg','password':'doualacameroun'})
            response = views.login(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_EMAIL, response.get("errCode"))


        #
        # TESTING PROFILE VIEW
        #

        #good profile view... valid user
        def testProfView1(self):
            testUser = testUtils.genUser()
            testApi = testUser.apikey
            newrequest = views.request
            newrequest.body = json.dumps({"apikey" : testApi})
            response = views.getProfile(newrequest)
            response = json.loads(response.content)
            print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))

        #bad profile view... invalid user
        def testProfView2(self):
            testUser = testUtils.genUser()
            testApi = testUser.apikey
            newrequest = views.request
            newrequest.body = json.dumps({"apikey" : "2340298304823094"})
            response = views.getProfile(newrequest)
            response = json.loads(response.content)
            print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_APIKEY, response.get("errCode"))

        #good profile view... valid driver
        def testProfView3(self):
            testUser = testUtils.genDriver()
            testApi = testUser.driver.apikey
            newrequest = views.request
            newrequest.body = json.dumps({"apikey" : testApi})
            response = views.getProfile(newrequest)
            response = json.loads(response.content)
            print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))


        #
        #TESTING CHANGIN PASSWORD
        #

        #good change valid user
        def testPassChange1(self):
            testUser = testUtils.genUser()
            testApi = testUser.apikey
            testPW = testUser.password
            newPW = "cs169pw"
            testEmail = testUser.email

            newrequest = views.request
            newrequest.body = json.dumps({"apikey" : testApi, "email" : testEmail, "currentpw" : testPW, "newpw" : newPW})
            response = views.changePassword(newrequest)
            response = json.loads(response.content)
            print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))



        #good change valid driver
        def testPassChange2(self):
            testDriver = testUtils.genDriver()
            testUser = testDriver.driver
            testApi = testUser.apikey
            testPW = testUser.password
            newPW = "cs169pw"
            testEmail = testUser.email

            newrequest = views.request
            newrequest.body = json.dumps({"apikey" : testApi, "email" : testEmail, "currentpw" : testPW, "newpw" : newPW})
            response = views.changePassword(newrequest)
            response = json.loads(response.content)
            print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))


        #bad change invalid api
        def testPassChange3(self):
            testDriver = testUtils.genDriver()
            testUser = testDriver.driver
            testApi = testUser.apikey
            testPW = testUser.password
            newPW = "cs169pw"
            testEmail = testUser.email

            newrequest = views.request
            newrequest.body = json.dumps({"apikey" : "23904029342", "email" : testEmail, "currentpw" : testPW, "newpw" : newPW})
            response = views.changePassword(newrequest)
            response = json.loads(response.content)
            print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_APIKEY, response.get("errCode"))



        #bad change bad email
        def testPassChange4(self):
            testDriver = testUtils.genDriver()
            testUser = testDriver.driver
            testApi = testUser.apikey
            testPW = testUser.password
            newPW = "cs169pw"
            testEmail = testUser.email

            newrequest = views.request
            newrequest.body = json.dumps({"apikey" : testApi, "email" : "somebs@bs.com", "currentpw" : testPW, "newpw" : newPW})
            response = views.changePassword(newrequest)
            response = json.loads(response.content)
            print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_CREDENTIALS, response.get("errCode"))


        #bad change bad currentpw
        def testPassChange5(self):
            testDriver = testUtils.genDriver()
            testUser = testDriver.driver
            testApi = testUser.apikey
            testPW = testUser.password
            newPW = "cs169pw"
            testEmail = testUser.email

            newrequest = views.request
            newrequest.body = json.dumps({"apikey" : testApi, "email" : testEmail, "currentpw" : "badpw", "newpw" : newPW})
            response = views.changePassword(newrequest)
            response = json.loads(response.content)
            print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_CREDENTIALS, response.get("errCode"))


        #bad new password 
        def testPassChange6(self):
            testDriver = testUtils.genDriver()
            testUser = testDriver.driver
            testApi = testUser.apikey
            testPW = testUser.password
            newPW = "cs169pw"
            testEmail = testUser.email

            newrequest = views.request
            newrequest.body = json.dumps({"apikey" : testApi, "email" : testEmail, "currentpw" : testPW, "newpw" : "wwwaaaaaaaaaaaaaayyyyyyyyyyyyyyyyttoooooooooolongggggggggggggggg"})
            response = views.changePassword(newrequest)
            response = json.loads(response.content)
            print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_INPUT_OR_LENGTH, response.get("errCode"))

        #
        #TESTING SEARCH 
        #

        #good search request
        def testSearch1(self):
            newrequest = views.request
            testRide= testUtils.genRide()
            departLocLat = testRide.depart_lat
            departLocLong = testRide.depart_lg
            destLocLat = testRide.arrive_lat
            destLocLong = testRide.arrive_lg
            testDate = "bullcrapdate"
            testTime = "craptime"
            testThresh = "50"
            newrequest.body = json.dumps({ "depart-loc": {"lat" : departLocLat, "long" : departLocLong} , "dest-loc" : {"lat" : destLocLat, "long" : destLocLong} , "time-depart" : "0:36", "date":"04-09-2013", "dist-thresh" : testThresh} )
            response = views.search(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))

        #badly formed json request
        def testSearch2(self):
            newrequest = views.request
            testRide= testUtils.genRide()
            departLocLat = testRide.depart_lat
            departLocLong = testRide.depart_lg
            destLocLat = testRide.arrive_lat
            destLocLong = testRide.arrive_lg
            testDate = "bullcrapdate"
            testTime = "craptime"
            testThresh = "50"
            newrequest = json.dumps({ "depart-loc": {"lat" : departLocLat, "long" : departLocLong} , "dest-loc" : {"lat" : destLocLat, "long" : destLocLong} , "time-depart" : "0:36", "date":"04-09-2013", "dist-thresh" : testThresh} )
            response = views.search(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_JSON, response.get("errCode"))


        #
        #TESTING MANAGE ROUTES 
        #

        #good manageRoute request
        def testManageRoutes1(self):
            newrequest = views.request
            testRide= testUtils.genRide()
            testApi = testRide.driver_info.driver.apikey
            newrequest.body = json.dumps({ "apikey" : testApi })
            response = views.manageRoute(newrequest)
            response = json.loads(response.content)
            print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))

        #bad manageRoute request, api invalid
        def testManageRoutes2(self):
            newrequest = views.request
            testRide= testUtils.genRide()
            testApi = testRide.driver_info.driver.apikey
            newrequest.body = json.dumps({ "apikey" : "23094802394029352" })
            response = views.manageRoute(newrequest)
            response = json.loads(response.content)
            print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_APIKEY, response.get("errCode"))


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
        #CHECK ROUTE DELETION
        #
        def testDeleteRoute1(self):
            newrequest = views.request
            testRoute = testUtils.genRide()
            testRouteId = testRoute.id
            testDriverApi = testRoute.driver_info.driver.apikey
            newrequest.body = json.dumps({ 'apikey' : testDriverApi, 'route_id' : testRouteId })
            response = views.delete_route(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))


        #
        #CHECK MANAGING REQUESTS
        #
        def testManageRequestsDriver1(self):
            newrequest = views.request
            testDriver = testUtils.genDriver()
    
            testRider = testUtils.genUser()
            testRide = testUtils.genRide()
            testId = testRide.id
            testApi = testRide.driver_info.driver.apikey
            departLocLat = testRide.depart_lat
            departLocLong = testRide.depart_lg
            destLocLat = testRide.arrive_lat
            destLocLong = testRide.arrive_lg

            newrequest.body = json.dumps({ "apikey" : testRider.apikey , "route_id" : testId, "depart-loc": {"lat" : departLocLat, "long" : departLocLong} , "dest-loc" : {"lat" : destLocLat, "long" : destLocLong} , "rider_depart_loc": {"rider_d_lat" : departLocLat, "rider_d_long" : departLocLong} , "rider_arrive_loc" : {"rider_a_lat" : destLocLat, "rider_a_long" : destLocLong}, "depart_time" : "0:36", "date":"04-09-2013", "rider_depart_time" : "0:38"} )
            response = views.select_ride(newrequest)
            #print response
            newrequest.body = json.dumps({'apikey' : testApi})
            #print (newrequest)
            #print("!!!!!!!!!!!!!!!!!!!!" + str(response))
            #print(response)
            response = views.manageRequest(newrequest)
            response = json.loads(response.content)

            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))


        def testManageRequestsRiderPending1(self):
            newrequest = views.request
            
            testRider = testUtils.genUser()
            testRide = testUtils.genRide()
            testId = testRide.id
            testApi = testRider.apikey
            departLocLat = testRide.depart_lat
            departLocLong = testRide.depart_lg
            destLocLat = testRide.arrive_lat
            destLocLong = testRide.arrive_lg

            newrequest.body = json.dumps({ "apikey" : testApi , "route_id" : testId, "depart-loc": {"lat" : departLocLat, "long" : departLocLong} , "dest-loc" : {"lat" : destLocLat, "long" : destLocLong} , "rider_depart_loc": {"rider_d_lat" : departLocLat, "rider_d_long" : departLocLong} , "rider_arrive_loc" : {"rider_a_lat" : destLocLat, "rider_a_long" : destLocLong}, "depart_time" : "0:36", "date":"04-09-2013", "rider_depart_time" : "0:38"} )
            response = views.select_ride(newrequest)
            #print response
            newrequest.body = json.dumps({'apikey' : testApi})
            response = views.managePendingRequest(newrequest)
            response = json.loads(response.content)
            #print "!!!!!!!!!!!!!" + str(response.get("errMsg"))
            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))



        def testManageRequestsRiderAccepted1(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide = testUtils.genRide()
            testId = testRide.id
            testApi = testRider.apikey
            departLocLat = testRide.depart_lat
            departLocLong = testRide.depart_lg
            destLocLat = testRide.arrive_lat
            destLocLong = testRide.arrive_lg

            newrequest.body = json.dumps({ "apikey" : testApi , "route_id" : testId, "depart-loc": {"lat" : departLocLat, "long" : departLocLong} , "dest-loc" : {"lat" : destLocLat, "long" : destLocLong} , "rider_depart_loc": {"rider_d_lat" : departLocLat, "rider_d_long" : departLocLong} , "rider_arrive_loc" : {"rider_a_lat" : destLocLat, "rider_a_long" : destLocLong}, "depart_time" : "0:36", "date":"04-09-2013", "rider_depart_time" : "0:38"} )
            response = views.select_ride(newrequest)
            #print response
            newrequest.body = json.dumps({'apikey' : testApi})
            response = views.manageAcceptedRequest(newrequest)
            response = json.loads(response.content)
            #print "!!!!!!!!!!!!!" + str(response.get("errMsg"))
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
                fields = ["firstname", "lastname", "email", "dob", "sex", "password", "cellphone", "user_type", "comments", "avg_rating"]
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



 #test select ride with good inputs
        def testGoodSelectRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))
        #test select ride wich user does not exist
        def testNotUserSelectRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            newrequest.body = json.dumps({ 'apikey' : "aaaa","route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_APIKEY, response.get("errCode"))
        #test select ride wich route does not exists
        def testNotRouteSelectRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":40000,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            #print(response)
            self.assertEquals(testLib.RestTestCase.ERR_UNKNOWN_ROUTE, response.get("errCode"))
        #test select ride wich already exists 
        def testAlreadyExistsSelectRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            prev_api = testApi
            prev_route_id = testRouteID
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            newrequest.body = json.dumps({ 'apikey' : prev_api,"route_id":prev_route_id,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response1 = views.select_ride(newrequest)
            response1 = json.loads(response1.content)

            self.assertEquals(testLib.RestTestCase.ERR_REQUEST_EXISTS, response1.get("errCode"))

        #test pass  accept_ride
        def testGoodAcceptRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            accept_request = views.request
            accept_request.body =json.dumps({"route_id":testRouteID,"response":1,"from":testApi,"to":driver_id})
            response1 = views.accept_ride(accept_request)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response1.get("errCode"))

        #test fail because of bad route  accept_ride
        def testBadRouteAcceptRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            accept_request = views.request
            accept_request.body =json.dumps({"route_id":3000,"response":1,"from":testApi,"to":driver_id})
            response1 = views.accept_ride(accept_request)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.ERR_UNKNOWN_ROUTE, response1.get("errCode"))

        #test fail because of bad rider apikey  accept_ride
        def testBadRiderAPIKEYAcceptRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            accept_request = views.request
            accept_request.body =json.dumps({"route_id":testRouteID,"response":1,"from":"AAAA","to":driver_id})
            response1 = views.accept_ride(accept_request)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_APIKEY, response1.get("errCode"))



        
        #test fail because of bad driver_info id  accept_ride
        def testBadDriverInfoIDAcceptRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            accept_request = views.request
            accept_request.body =json.dumps({"route_id":testRouteID,"response":1,"from":testApi,"to":600000})
            response1 = views.accept_ride(accept_request)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.ERR_UNKNOWN_DRIVER, response1.get("errCode"))

        #test pass  accept_ride
        def testGoodDenyRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            accept_request = views.request
            accept_request.body =json.dumps({"route_id":testRouteID,"response":0,"from":testApi,"to":driver_id})
            response1 = views.accept_ride(accept_request)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response1.get("errCode"))

        #test fail because of bad route  accept_ride
        def testBadRouteDenyRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            accept_request = views.request
            accept_request.body =json.dumps({"route_id":3000,"response":0,"from":testApi,"to":driver_id})
            response1 = views.accept_ride(accept_request)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.ERR_UNKNOWN_ROUTE, response1.get("errCode"))

        #test fail because of bad rider apikey  accept_ride
        def testBadRiderAPIKEYDenyRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            accept_request = views.request
            accept_request.body =json.dumps({"route_id":testRouteID,"response":0,"from":"AAAA","to":driver_id})
            response1 = views.accept_ride(accept_request)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_APIKEY, response1.get("errCode"))



        #test fail because of bad driver_info id  accept_ride
        def testBadDriverInfoIDDenyRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            accept_request = views.request
            accept_request.body =json.dumps({"route_id":testRouteID,"response":0,"from":testApi,"to":600000})
            response1 = views.accept_ride(accept_request)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.ERR_UNKNOWN_DRIVER, response1.get("errCode"))

        #test  past good cancel request
        def testGoodCancelRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            cancel_rq = views.request
            cancel_rq.body =json.dumps({"route_id":testRouteID,"apikey":testApi})
            response1 = views.cancel_request(cancel_rq)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response1.get("errCode"))
 #test fails because of bad route
        def testBadRouteCancelRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            cancel_rq = views.request
            cancel_rq.body =json.dumps({"route_id":800000,"apikey":testApi})
            response1 = views.cancel_request(cancel_rq)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.ERR_UNKNOWN_ROUTE, response1.get("errCode"))
        #test  past good cancel request
        def testBadApiKeyCancelRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            cancel_rq = views.request
            cancel_rq.body =json.dumps({"route_id":testRouteID,"apikey":"blahblah"})
            response1 = views.cancel_request(cancel_rq)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_APIKEY, response1.get("errCode"))
        #test  past good cancel request
        def testBadRequestCancelRide(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRider1 = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testApi1 = testRider1.apikey

            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            cancel_rq = views.request
            cancel_rq.body =json.dumps({"route_id":testRouteID,"apikey":testApi1})
            response1 = views.cancel_request(cancel_rq)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.ERR_NO_RIDER_DRIVER_CONTACT, response1.get("errCode"))




        #test  past good leave feedback
        def testGoodFeedback(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            feedback_rq = views.request
            feedback_rq.body =json.dumps({"route_id":testRouteID,"apikey":testApi,"rating":4,"comment":"such a good driver"})
            response1 = views.cancel_request(feedback_rq)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response1.get("errCode"))

        #test fails because of bad route
        def testBadRouteFeedBack(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            feedback_rq = views.request
            feedback_rq.body =json.dumps({"route_id":800000,"apikey":testApi,"rating":4,"comment":"such a good driver"})
            response1 = views.leave_feedback(feedback_rq)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.ERR_UNKNOWN_ROUTE, response1.get("errCode"))
        #test  fails bad apikey
        def testBadApiKeyLeaveFeedback(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            feedback_rq = views.request
            feedback_rq.body =json.dumps({"route_id":testRouteID,"apikey":"blahblah","rating":4,"comment":"such a good driver"})
            response1 = views.leave_feedback(feedback_rq)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.ERR_BAD_APIKEY, response1.get("errCode"))
        #test  fails because of no request history
        def testBadRequestLeaveFeeback(self):
            newrequest = views.request
            testRider = testUtils.genUser()
            testRider1 = testUtils.genUser()
            testRide  = testUtils.genRide()
            testApi = testRider.apikey
            testApi1 = testRider1.apikey

            testRouteID = testRide.id
            driver_id = testRide.driver_info.driver.id
            newrequest.body = json.dumps({ 'apikey' : testApi,"route_id":testRouteID,"rider_depart-loc":{"rider_d_lat":"00000","rider_d_long":"99999"},"rider_arrive_loc":{"rider_a_lat":"88888","rider_a_long":"77777"},"rider_depart_time":"11:37:25"} )
            response = views.select_ride(newrequest)
            response = json.loads(response.content)
            feedback_rq = views.request
            feedback_rq.body =json.dumps({"route_id":testRouteID,"apikey":testApi1,"rating":4,"comment":"such a good driver"})
            response1 = views.cancel_request(feedback_rq)
            response1 = json.loads(response1.content)
            self.assertEquals(testLib.RestTestCase.ERR_NO_RIDER_DRIVER_CONTACT, response1.get("errCode"))


