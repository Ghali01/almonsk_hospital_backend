from django.db import models
from doctors.models import Doctor
from drugs.models import Drug
from surgeries.models import Surgery

class Patient(models.Model):
    familyChoices=[ 
        ('S','Single'),
        ('M','Married'),
    ]
    genderChoices=[ 
        ('F','Female'),
        ('M','Male'),
    ]
    firstName=models.CharField(max_length=15)
    motherName=models.CharField(max_length=15)
    fatherName=models.CharField(max_length=15)
    secondName=models.CharField(max_length=15)
    nationality=models.CharField(max_length=15,null=True)
    occupation=models.CharField(max_length=15,null=True)
    phone=models.CharField(max_length=10)
    address=models.CharField(max_length=100)
    attendantName=models.CharField(max_length=50)
    attendantPhone=models.CharField(max_length=10)
    attendantAdderss=models.CharField(max_length=100)
    room=models.IntegerField()
    therapy=models.CharField(max_length=30)
    acceptID=models.IntegerField()
    enter=models.DateTimeField()
    out=models.DateTimeField()
    birth=models.DateField()
    gender=models.CharField(max_length=1,choices=genderChoices)
    family=models.CharField(max_length=1,choices=familyChoices)
    doctor=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL,related_name='patients')
    consults=models.ManyToManyField(Doctor,through='PatientConsult')
class patientCosts(models.Model):
    patient=models.OneToOneField(Patient,on_delete=models.CASCADE)
    surgeryRom=models.PositiveIntegerField(null=True)
    residence=models.PositiveIntegerField(null=True)
    serums=models.PositiveIntegerField(null=True)
    arches=models.PositiveIntegerField(null=True)
    threads=models.PositiveIntegerField(null=True)
    plastic=models.PositiveIntegerField(null=True)
    laboratory=models.PositiveIntegerField(null=True)
    rays=models.PositiveIntegerField(null=True)
    ECG=models.PositiveIntegerField(null=True)
    resuscitate=models.PositiveIntegerField(null=True)
    monitor=models.PositiveIntegerField(null=True)
    echo=models.PositiveIntegerField(null=True)
    axial=models.PositiveIntegerField(null=True)
    incubator=models.PositiveIntegerField(null=True)
    gypsum=models.PositiveIntegerField(null=True)
    plates=models.PositiveIntegerField(null=True)
    bandages=models.PositiveIntegerField(null=True)
    intensiveCare=models.PositiveIntegerField(null=True)
    service=models.PositiveIntegerField(null=True)

class PatientConsult(models.Model):
    doctor=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL)
    patient=models.ForeignKey(Patient,null=True,on_delete=models.SET_NULL)
    cost=models.PositiveIntegerField()


class PatientDrugs(models.Model):
    drug=models.ForeignKey(Drug,null=True,on_delete=models.SET_NULL)
    patient=models.ForeignKey(Patient,null=True,on_delete=models.SET_NULL)
    count=models.PositiveIntegerField()
    price=models.PositiveIntegerField()
    note=models.CharField(max_length=200)


class PatientSurgery(models.Model):
    patient=models.ForeignKey(Patient,null=True,on_delete=models.SET_NULL)
    surgery=models.ForeignKey(Surgery,on_delete=models.SET_NULL,null=True)
    surgeon=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL,related_name='surgerisAsSergeon')
    assistant=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL,related_name='surgeriesAsAssistant')
    anesthetic=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL,related_name='surgeriesAsAnesthetic')
    surgeonCosts=models.PositiveIntegerField()
    assistantCosts=models.PositiveIntegerField()
    anestheticCosts=models.PositiveIntegerField()
    start=models.TimeField()
    end=models.TimeField()
    price=models.PositiveIntegerField()
