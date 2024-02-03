from rest_framework import  serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from django.db.models import F,Sum
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
    drugs=SerializerMethodField()
    surgeonCosts=SerializerMethodField()
    assistantCosts=SerializerMethodField()
    anestheticCosts=SerializerMethodField()

    class Meta:
        model=patientCosts
        exclude=['patient','id']

    def  get_drugs(self,obj):
        drugs=PatientDrug.objects.filter(patient_id=obj.patient.id,discrete=False).annotate(total=F('price')*F('count')).aggregate(allTotal=Sum('total'))['allTotal']
        return drugs
    
    def get_surgeonCosts(self,obj):
        costs=PatientSurgery.objects.filter(patient_id=obj.patient.id).aggregate(costs=Sum('surgeonCosts'))['costs']
        return costs
    def get_surgeonCosts(self,obj):
        costs=PatientSurgery.objects.filter(patient_id=obj.patient.id).aggregate(costs=Sum('surgeonCosts'))['costs']
        return costs
    def get_assistantCosts(self,obj):
        costs=PatientSurgery.objects.filter(patient_id=obj.patient.id).aggregate(costs=Sum('assistantCosts'))['costs']
        return costs
    def get_anestheticCosts(self,obj):
        costs=PatientSurgery.objects.filter(patient_id=obj.patient.id).aggregate(costs=Sum('anestheticCosts'))['costs']
        return costs
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