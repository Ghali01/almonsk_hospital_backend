from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Doctor
from rest_framework.fields import IntegerField
class DoctorSerialzer(ModelSerializer):
    account= IntegerField(read_only=True)
    class Meta:
        model=Doctor
        fields=['id','firstName','fatherName','secondName','phone','account']
        read_only_fields=['account']   