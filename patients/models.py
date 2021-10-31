from django.db import models
from django.db.models.fields import PositiveIntegerField
from doctors.models import Doctor
from drugs.models import Drug
from surgeries.models import Surgery

class Patient(models.Model):
    firstName=models.CharField(max_length=15)
    motherName=models.CharField(max_length=15)
    fatherName=models.CharField(max_length=15)
    secondName=models.CharField(max_length=15)
    birth=models.DateField()
    nationality=models.CharField(max_length=15,null=True)
    occupation=models.CharField(max_length=15,null=True)
    phone=models.CharField(max_length=10)
    address=models.CharField(max_length=100)
    attendantName=models.CharField(max_length=15)
    attendantPhone=models.CharField(max_length=10)
    attendantAdderss=models.CharField(max_length=100)
    room=models.IntegerField()
    therapy=models.CharField(max_length=30)
    acceptID=models.IntegerField()
    doctor=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL,related_name='patients')
    consults=models.ManyToManyField(Doctor,through='PatientConsult')
 
class patientCosts(models.Model):
    patient=models.OneToOneField(Patient,on_delete=models.CASCADE)
    surgeon=PositiveIntegerField(null=True)
    assistant=PositiveIntegerField(null=True)
    sedated=PositiveIntegerField(null=True)
    surgeryRom=PositiveIntegerField(null=True)
    residence=PositiveIntegerField(null=True)
    serums=PositiveIntegerField(null=True)
    arches=PositiveIntegerField(null=True)
    threads=PositiveIntegerField(null=True)
    plastic=PositiveIntegerField(null=True)
    laboratory=PositiveIntegerField(null=True)
    rays=PositiveIntegerField(null=True)
    ECG=PositiveIntegerField(null=True)
    resuscitate=PositiveIntegerField(null=True)
    monitor=PositiveIntegerField(null=True)
    echo=PositiveIntegerField(null=True)
    axial=PositiveIntegerField(null=True)
    incubator=PositiveIntegerField(null=True)
    gypsum=PositiveIntegerField(null=True)
    plates=PositiveIntegerField(null=True)
    bandages=PositiveIntegerField(null=True)
    intensiveCare=PositiveIntegerField(null=True)
    service=PositiveIntegerField(null=True)

class PatientConsult(models.Model):
    doctor=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL)
    patient=models.ForeignKey(Patient,null=True,on_delete=models.SET_NULL)
    cost=models.PositiveIntegerField()


class PatientDrugs(models.Model):
    drug=models.ForeignKey(Drug,null=True,on_delete=models.SET_NULL)
    patient=models.ForeignKey(Patient,null=True,on_delete=models.SET_NULL)
    count=models.PositiveIntegerField()
    price=PositiveIntegerField()
    note=models.CharField(max_length=200)


class PatientSurgery(models.Model):
    patient=models.ForeignKey(Patient,null=True,on_delete=models.SET_NULL)
    surgeon=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL,related_name='surgerisAsSergeon')
    assistant=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL,related_name='surgeriesAsAssistant')
    start=models.TimeField()
    end=models.TimeField()
    price=PositiveIntegerField()
