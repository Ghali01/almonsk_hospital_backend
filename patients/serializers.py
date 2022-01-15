from rest_framework import  serializers
from rest_framework.serializers import ModelSerializer
from .models import *

class PatientListSerializer(ModelSerializer):

    class Meta:
        model=Patient
        fields=['id','firstName','fatherName','motherName','secondName','acceptID','locked']

        
class PatientAcceptSerializer(ModelSerializer):

    class Meta:
        model=Patient
        fields=['id','firstName','fatherName','motherName','secondName','nationality','occupation','phone',
                'address','attendantName','attendantPhone','attendantAdderss',
                'enterDate','enterTime','outDate','outTime','birth','room','therapy',
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
    miscellaneous=serializers.IntegerField(source='costs.invoiceMisc')
    class Meta:
        model=Patient
        fields=['fullName','doctorName','surgeryRom','intensiveCare','residence',
                    'laboratory','miscellaneous','gender','acceptID','enterDate','outDate']