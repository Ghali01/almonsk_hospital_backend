from django.db import models
from django.db.models.fields import PositiveIntegerField
class Surgery(models.Model):
    name=models.CharField(max_length=100)
    price=PositiveIntegerField()
    duration =models.FloatField()
   
    class Meta:
        ordering=['name']