from django.db import models
from django.db.models.functions.datetime import datetime
from django.utils import timezone



class garb(models.Model):
    file_name = models.TextField()
    ident = models.IntegerField(default=0)
    cord_x = models.IntegerField(default=0)
    cord_y = models.IntegerField(default=0)

    def __str__(self):
        return self.file_name


class request(models.Model):
    date = models.DateField()
    request_date = models.DateTimeField(default=timezone.now)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    json = models.TextField()
    res_file_name_m = models.TextField(default='-')
    res_file_name_f = models.TextField(default='-')

    def __str__(self):
        return self.date.__str__() + '_' + self.lat.__str__() + '_' + self.lon.__str__()

