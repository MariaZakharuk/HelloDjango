from django.db import models

# Create your models here.
class point(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    name = models.CharField(max_length= 25)