from django.db import models
from django.db.models.fields import BooleanField
from doctors.models import Doctor
from drugs.models import Drug,Employee
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
    phone=models.CharField(max_length=10,null=True)
    address=models.CharField(max_length=100,null=True)
    attendantName=models.CharField(max_length=50,null=True)
    attendantPhone=models.CharField(max_length=10,null=True)
    attendantAdderss=models.CharField(max_length=100,null=True)
    room=models.IntegerField(null=True)
    therapy=models.CharField(max_length=30,null=True)
    acceptID=models.IntegerField()
    enter=models.DateTimeField()
    out=models.DateTimeField(null=True)
    birth=models.DateField(null=True)
    gender=models.CharField(max_length=1,choices=genderChoices)
    family=models.CharField(max_length=1,choices=familyChoices)
    doctor=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL,related_name='patients')
    consults=models.ManyToManyField(Doctor,through='PatientConsult')
    class Meta:
        ordering=['-id']
    
    def __str__(self):
        return f'{self.firstName} {self.fatherName} {self.secondName}'
class patientCosts(models.Model):
    patient=models.OneToOneField(Patient,on_delete=models.CASCADE,related_name='costs')
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
    paided=BooleanField(default=False)


class PatientDrug(models.Model):
    drug=models.ForeignKey(Drug,null=True,on_delete=models.SET_NULL)
    patient=models.ForeignKey(Patient,null=True,on_delete=models.SET_NULL,related_name='drugs')
    count=models.PositiveIntegerField()
    price=models.PositiveIntegerField()
    note=models.CharField(max_length=200,null=True)
    date=models.DateField()
    employee=models.ForeignKey(Employee,null=True,on_delete=models.SET_NULL)



class PatientSurgery(models.Model):
    patient=models.ForeignKey(Patient,null=True,on_delete=models.SET_NULL)
    surgery=models.ForeignKey(Surgery,on_delete=models.SET_NULL,null=True)
    surgeon=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL,related_name='surgerisAsSergeon')
    assistant=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL,related_name='surgeriesAsAssistant')
    anesthetic=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL,related_name='surgeriesAsAnesthetic')
    surgeonCosts=models.PositiveIntegerField(null=True)
    assistantCosts=models.PositiveIntegerField(null=True)
    anestheticCosts=models.PositiveIntegerField(null=True)
    start=models.TimeField()
    end=models.TimeField()
    price=models.PositiveIntegerField()
    surgeonPaided=BooleanField(default=False)
    assistantPaided=BooleanField(default=False)
    anestheticPaided=BooleanField(default=False)
