from django.db import models

class garb(models.Model):
    file_name = models.CharField(max_length=300)
    ident = models.IntegerField(default=0)
    cord_x = models.IntegerField(default=0)
    cord_y = models.IntegerField(default=0)

    def __str__(self):
        return self.file_name

class request(models.Model):
    date = models.DateField()
    city = models.CharField(max_length=200)
    json = models.CharField(max_length=500, default="none")
    res_file_name = models.CharField(max_length=100)

    def __str__(self):
        return self.date.__str__() + '_' + self.city.__str__()

