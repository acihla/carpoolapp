"""
Unit tests for the server.py module.
This is just a sample. You should have more tests for your model (at least 10)
"""

import unittest
import os
import testLib
import sys
import models
import views
from datetime import *


test_date = date(1992,4,17)


class UnitTest(unittest.TestCase):
    """
    Unittests for the Users model class (a sample, incomplete)
    """
    

    def setUp(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = "mysite.settings"
        self.users = models.User()
        self.routes = models.Route()

        
    def testAddRoute(self):
        """
        Tests that adding a user works
        """
        self.assertEquals(1, views.handleRouteData(1, "fremont", "san jose", test_date))
    def testSelectRoute(self):
      """
        Tests that i can select a route
      """
      self.assertEquals(1, views.select_ride({"rider_id":1, "route_id"=2})

    def testSelectRoute(self):

# If this file is invoked as a Python script, run the tests in this module
if __name__ == "__main__":
    # Add a verbose argument
    sys.argv = [sys.argv[0]] + ["-v"] + sys.argv[1:]
    unittest.main()
