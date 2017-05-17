from django.db import models
from django_permanent.models import PermanentModel
from process.helpers import region_hash

# Create your models here.
class CarRecord(PermanentModel):
    car_id = models.IntegerField('car_id',default=-1)
    route_id = models.IntegerField('route_id',default=-1)
    time = models.DateTimeField('time')
    longitude = models.DecimalField('lon',max_digits=10,decimal_places=7)
    latitude = models.DecimalField('lat',max_digits=10,decimal_places=7)
    region = models.SmallIntegerField('region', default=0)
    def __unicode__(self):
        return u'区县:' + region_hash[self.region]+ u', 经度:'+str(self.longitude) + u', 纬度:' + str(self.latitude) + u', 时间:' + str(self.time) +u'\n'