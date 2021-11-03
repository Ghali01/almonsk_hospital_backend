from rest_framework import fields, serializers
from rest_framework.serializers import Serializer,ModelSerializer
from doctors.serializers import DoctorSerialzer
from .models import *

class PatientListSerializer(ModelSerializer):

    class Meta:
        model=Patient
        fields=['id','firstName','fatherName','motherName','secondName','acceptID']

        
class PatientAcceptSerializer(ModelSerializer):

    class Meta:
        model=Patient
        fields=['id','firstName','fatherName','motherName','secondName','nationality','occupation','phone',
                'address','attendantName','attendantPhone','attendantAdderss',
                'enter','out','birth','room','therapy',
                'gender','family','doctor','doctor','acceptID']

    def create(self, validated_data):
        patient= super().create(validated_data)
        patientCosts.objects.create(patient=patient)
        return patient
class ConsultSerializer(ModelSerializer):
    class Meta:
        model=PatientConsult
        fields=['doctor','cost','patient']
class PatientCostSerializer(ModelSerializer):
    class Meta:
        model=patientCosts
        exclude=['patient','id']

