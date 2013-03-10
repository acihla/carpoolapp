#Alexander Cihla: Splunk quick proj

import sys
import os
from googlemaps import GoogleMaps

#connecting using api key for alex.cihla@gmail.com
gmaps = GoogleMaps("AIzaSyAGf-Mbj40HtzmRmOvPWZX4RnE2RIG_tzc")

#grabbing array of arguments including start and end locations
cities = sys.argv[1:]

k = 0
for loc in cities:
	if loc != "to":
		k += 1
	else:
		format = 'true'
		break

if format != 'true':
	print "\n \n***************************************************************************************************************************************************************"
	print "Your request format is flawed. Submit arguments in the following manner <start> to <destination>  \nYour command should look like this >>$  python escape.py <My Start Location> to <My End Location>"
	print "*************************************************************************************************************************************************************** \n \n"
	exit(-1)

#stitching together start point string
start = ' '.join(map(str, cities[:k]))

k += 1

#stitching together destination point string
end = ' '.join(map(str, cities[k:]))

#collecting means of transportation from user
sys.stdout.write("How do you wish to travel? Use (driving, walking, or bicycling) \n")
mode = raw_input().lower()
if mode not in {'driving', 'walking', 'bicycling'}:
	print 'That is not an approved means... we will assume that you are driving yourself.'

#collecting waypoint of user
waypoint = []
sys.stdout.write("Would you like to use a waypoint? y/n \n")
if raw_input().lower() == 'y':
	sys.stdout.write("Enter the place through which you would like to travel... \n")
	waypoint.append(raw_input().lower())
else:
	waypoint.append('')


try:

	#making googlemaps directions request and finding the list of possible legs of travel
	primRoute = gmaps.directions(start, end, mode, waypoint)
	route = primRoute['routes'][0]
	legs = route['legs']

	#some encouraging device
	print "\n \n***************************************************************************************************************"
	print "Hurry... we are routing you from " +start+ " to " +end+ ". Good luck!"

	#dealing with possible multiple legs due to utilization of a waypoint
	for trip in legs:
		#print primRoute['routes'][end_location]
		#printing time and distance of route
		routeTime = trip['duration']['value'] / 60
		routeDist = trip['distance']['value'] * 0.000621371
		print "\n\nThis route will take " +str(routeTime)+ " minutes to travel " +str(routeDist)+ " miles at legal speeds... think you can do better?"
		print "***************************************************************************************************************"
		print "********************************************************************************************************"
		print "************************************************************************************************"
		print "******VVDirectionsVV*******************************************************************\n"
		
		#formatting and printing each step

		for step in trip['steps']:
			indstep = step['html_instructions']
			indstep = indstep.replace('</b>', '')
			indstep = indstep.replace('<b>', '')
			indstep = indstep.replace('/<wbr/>', '')
			indstep = indstep.replace('<div style="font-size:0.9em">', ' *** ')
			indstep = indstep.replace('<div class="">', ' *** ')
			indstep = indstep.replace('<div class="google_note">', ' *** ')
			indstep = indstep.replace('</div>', ' *** ')
			print indstep

	print "\nYou have arrived!"

#general error catching... not the most descriptive and definite room for improvement
except Exception, err:
	print "\n \n***************************************************************************************************************************************************************"
	print "Your locations are not recognized by the system... " +start+ " to " +end+ " is not a known legitimate route! Try entering less specific information"
	print "*************************************************************************************************************************************************************** \n \n"
	print "The specific error is... " +str(err)
	