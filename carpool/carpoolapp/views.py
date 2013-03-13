from django.utils import simplejson as json
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder

from carpoolapp.models import User, DriverInfo, Rating, Route

def search(request):
	routes = Route.objects.all()
	resp = {"error":"Success"}
	rides = []
	for route in routes:
		entry = {}
		entry["driver"] = route.driver
		entry["rider"] = route.rider
		entry["depart_time"] = route.depart_time
		entry["arrival_time"] = route.depart_time
		entry["depart_lat"] = route.depart_lat
		entry["depart_lg"] = route.depart_lg
		entry["arrive_lat"] = route.arrive_lat
		entry["arrive_lg"] = route.arrive_lg
		entry["status"] = route.status

		rides.append(entry)


	resp["rides"] = rides
	return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")