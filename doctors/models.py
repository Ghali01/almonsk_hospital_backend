from django.db import models


class Doctor(models.Model):
    firstName=models.CharField(max_length=50)
    fatherName=models.CharField(max_length=50)
    secondName=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)