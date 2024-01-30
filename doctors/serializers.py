from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Doctor
from rest_framework.fields import IntegerField
class DoctorSerialzer(ModelSerializer):
    account= IntegerField(read_only=True)
    class Meta:
        model=Doctor
        fields=['id','firstName','fatherName','secondName','phone','specialzation','surgeon','assistant','anesthetic','account']
        read_only_fields=['account']   
class UpdateDoctorSerialzer(ModelSerializer):
    account= IntegerField(read_only=True)
    class Meta:
        model=Doctor
        fields=['id','firstName','fatherName','secondName','phone','specialzation','surgeon','assistant','anesthetic','account']
        read_only_fields=['firstName','fatherName','secondName','account']   
