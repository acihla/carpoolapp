from django.db import models


class User(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    dob = models.DateField()
    sex = models.CharField(max_length=10)
    password = models.CharField(max_length=200)
    cellphone = models.CharField(max_length=200)
    driver = models.BooleanField(default=0)
    comments = models.CharField(max_length=200)
    avg_rating = models.IntegerField()

    def __unicode__(self):
        return self.username

class DriverInfo(models.Model):
    driver = models.ForeignKey(User)
    license_no = models.CharField(max_length=200)
    license_exp = models.DateField()
    car_make = models.CharField(max_length=200)
    car_type = models.CharField(max_length=200)
    car_mileage = models.IntegerField(max_length=200)
    max_passengers = models.IntegerField(null=True)

    def __unicode__(self):
        return self.license_no

class Rating(models.Model):
	owner = models.ForeignKey(User)
	author = models.CharField(max_length=200)
	rating = models.IntegerField()
	comment = models.CharField(max_length=400)


class Route(models.Model):
    driver = models.ForeignKey(DriverInfo)
    rider = models.ForeignKey(User, null=True)
    depart_time = models.DateTimeField()
    #arrival_time = models.DateTimeField()
    #depart_lat = models.CharField(max_length=200)
    #depart_lg = models.CharField(max_length=200)
    #arrive_lat = models.CharField(max_length=200)
    #arrive_lg = models.CharField(max_length=200)
    maps_info = models.CharField(max_length=5000)
    status = models.BooleanField(default=0)

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

