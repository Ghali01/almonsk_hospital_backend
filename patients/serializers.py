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
        fields=['doctor','cost','paided','patient']
class PatientCostSerializer(ModelSerializer):
    class Meta:
        model=patientCosts
        exclude=['patient','id']

class PatientDrugSerializer(ModelSerializer):
    class Meta:
        model=PatientDrug
        fields='__all__'

class PatienSurgerySerializer(ModelSerializer):

    class Meta:
        model=PatientSurgery
        fields='__all__'

class InvoiceSerializer(ModelSerializer):
    doctorName=serializers.StringRelatedField(source='doctor')
    fullName=serializers.StringRelatedField(source='*')
    surgeryRom=serializers.IntegerField(source='costs.surgeryRom')
    intensiveCare=serializers.IntegerField(source='costs.intensiveCare')
    residence=serializers.IntegerField(source='costs.residence')
    laboratory=serializers.IntegerField(source='costs.laboratory')
    class Meta:
        model=Patient
        fields=['fullName','doctorName','surgeryRom','intensiveCare','residence',
                    'laboratory','gender','acceptID','enter','out']