from django.db import models
import random, sha


class User(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    #username = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    dob = models.DateField()
    sex = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    cellphone = models.CharField(max_length=20)
    #driverOrRider = models.CharField(max_length=64, default = "rider")
    driver = models.BooleanField(default=False)
    comments = models.CharField(default="", max_length=200)
    avg_rating = models.FloatField(default = 0)
    apikey = models.CharField(max_length=40)

    def __unicode__(self):
        return self.email

    def to_dict(self):
        rtn = {}
        rtn["id"] = self.id
        rtn["firstname"] = self.firstname
        rtn["lastname"] = self.lastname
        #rtn["username"] = self.username
        rtn["email"] = self.email
        rtn["dob"] = self.dob
        rtn["sex"] = self.sex
        rtn["cellphone"] = self.cellphone
        rtn["driver"] = self.driver
        rtn["comments"] = self.comments
        rtn["avg_rating"] = self.avg_rating
        return rtn

    def to_dict_unsecure(self):
        rtn = {}
        rtn["id"] = self.id
        rtn["firstname"] = self.firstname
        rtn["lastname"] = self.lastname
        #rtn["username"] = self.username
        rtn["email"] = self.email
        rtn["dob"] = self.dob
        rtn["sex"] = self.sex
        rtn["password"] = self.password
        rtn["cellphone"] = self.cellphone
        rtn["driver"] = self.driver
        rtn["comments"] = self.comments
        rtn["avg_rating"] = self.avg_rating
        rtn["apikey"] = self.apikey
        return rtn

    def generate_apikey(self):
        salt = sha.new(str(random.random())).hexdigest()[:5]
        return sha.new(salt+self.email).hexdigest()

class DriverInfo(models.Model):
    driver = models.ForeignKey(User)
    license_no = models.CharField(max_length=50)
    license_exp = models.DateField()
    car_make = models.CharField(max_length=20)
    car_type = models.CharField(max_length=20)
    car_mileage = models.IntegerField()
    max_passengers = models.CharField(null=True, max_length=3)

    def __unicode__(self):
        return self.license_no

    def to_dict(self):
        rtn = {}
        rtn["id"] = self.id
        rtn["driver"] = self.driver.to_dict()
        rtn["license_no"] = self.license_no
        rtn["license_exp"] = self.license_exp
        rtn["car_make"] = self.car_make
        rtn["car_type"] = self.car_type
        rtn["car_mileage"] = self.car_mileage
        rtn["max_passengers"] = self.max_passengers

        return rtn

class Rating(models.Model):
    owner = models.ForeignKey(User)
    author = models.CharField(max_length=200)
    rating = models.IntegerField()
    comment = models.CharField(max_length=400)

    def to_dict(self):
        rtn = {}
        rtn["id"] = self.id
        rtn["owner"] = self.owner
        rtn["author"] = self.author
        rtn["rating"] = self.rating
        rtn["comment"] =  self.comment
        return rtn


class Route(models.Model):
    driver_info = models.ForeignKey(DriverInfo)
    rider = models.ForeignKey(User, null=True)
    depart_time = models.DateTimeField()
    #arrival_time = models.DateTimeField()
    depart_lat = models.CharField(max_length=15, null=True)
    depart_lg = models.CharField(max_length=15, null=True)
    arrive_lat = models.CharField(max_length=15, null=True)
    arrive_lg = models.CharField(max_length=15, null=True)
    maps_info = models.CharField(max_length=1000, default="")
    status = models.CharField(max_length=64, default=False)


    def to_dict(self):
        rtn = {}
        rtn["id"] = self.id
        rtn["driver_info"] = self.driver_info.to_dict()
        if self.rider != None:
            rtn["rider"] = self.rider.to_dict()
        rtn["depart_time"] = self.depart_time
        rtn["depart_lat"] = self.depart_lat
        rtn["depart_lg"] = self.depart_lg
        rtn["arrive_lat"] = self.arrive_lat
        rtn["arrive_lg"] = self.arrive_lg
        rtn["maps_info"] = self.maps_info
        rtn["status"] = self.status
        return rtn
class ride_request(models.Model):
      rider = models.ForeignKey(User, null=True)
      route_id = models.IntegerField()
      status = models.CharField(max_length=64)
      comment = models.CharField(max_length=400)


class SampleKey(models.Model):
    name = models.CharField(max_length=200)
    
class Sample(models.Model):
    driver = models.ForeignKey(SampleKey)
    rider = models.CharField(max_length=200)


#from http://djangosnippets.org/snippets/199/
def instance_dict(instance, key_format=None):
    """
    Returns a dictionary containing field names and values for the given
    instance
    """
    from django.db.models.fields import DateField
    from django.db.models.fields.related import ForeignKey
    if key_format:
        assert '%s' in key_format, 'key_format must contain a %s'
    key = lambda key: key_format and key_format % key or key

    pk = instance._get_pk_val()
    d = {}
    for field in instance._meta.fields:
        attr = field.name
        if hasattr(instance, attr):  # django filer broke without this check
            value = getattr(instance, attr)
            if value is not None:
                if isinstance(field, ForeignKey):
                    fkey_values = instance_dict(value)
                    for k, v in fkey_values.items():
                        d['%s.%s' % (key(attr), k)] = v
                        continue
                elif isinstance(field, DateField):
                    value = value.strftime('%Y-%m-%d')
        else:
            value = None
        d[key(attr)] = value
        
    for field in instance._meta.many_to_many:
        if pk:
            d[key(field.name)] = [
            obj._get_pk_val()
            for obj in getattr(instance, field.attname).all()]
        else:
            d[key(field.name)] = []
    return d

