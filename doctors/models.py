from django.db import models


class Doctor(models.Model):
    firstName=models.CharField(max_length=50)
    fatherName=models.CharField(max_length=50)
    secondName=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    specialzation=models.CharField(max_length=50)
    surgeon=models.BooleanField()
    assistant=models.BooleanField()
    anesthetic=models.BooleanField()
    
    class Meta:
        ordering=['firstName','fatherName','secondName']

    def __str__(self):
        return f'{self.firstName} {self.fatherName} {self.secondName}'