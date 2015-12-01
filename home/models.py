from django.db import models

# Create your models here.
class Temp_Node(models.Model):
    node = models.CharField(max_length=20)
    tags = models.CharField(max_length=10)
    date = models.DateTimeField() 
    temperature = models.FloatField()
    humidity = models.FloatField()
    l_flux = models.FloatField()