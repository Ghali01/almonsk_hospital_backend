
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.fields import IntegerField,CharField,DateTimeField
from rest_framework.relations import StringRelatedField
from .models import Material,Employee, Invoice, InvoiceItem
from django.db.models import F

class MaterialSerializer(ModelSerializer):
    class Meta:
        model=Material
        fields=['id','name','price','buyPrice','count']
        read_only_fields=['id','count']



class UpdateMaterialSerializer(ModelSerializer):
    class Meta:
        model=Material
        fields=['id','name','price','buyPrice','count']
        read_only_fields=['id','name','count']

class EmployeeSerializer(ModelSerializer):

    class Meta:
        model=Employee
        fields=['id','firstName','fatherName','secondName','inPermission','outPermission','phone']
class UpdateEmployeeSerializer(ModelSerializer):

    class Meta:
        model=Employee
        fields=['id','firstName','fatherName','secondName','inPermission','outPermission','phone']
        read_only_fields=['id','firstName','fatherName','secondName']




class InvoiceListSerializer(ModelSerializer):
    employeeName=CharField(source='employee.__str__',read_only=True)
    count =IntegerField()
    class Meta:
        model=Invoice 
        fields=['id','employee','employeeName','datetime','type','count']

class InvoiceItemInInvoiceSerializer(ModelSerializer):
    materialName= CharField(source='material.name',read_only=True)
    price=IntegerField(read_only=True)
    class Meta:
        model=InvoiceItem
        fields=['material','materialName','price','count']

class InvoiceSerializer(ModelSerializer):
    items=InvoiceItemInInvoiceSerializer(many=True)
    employeeName=CharField(source='employee.__str__',read_only=True)
    count =IntegerField(read_only=True)
    def create(self, validated_data):
        invoice=Invoice.objects.create(employee=validated_data['employee'],type=validated_data['type'])
        for item in validated_data['items']:
            if validated_data['type'] in ('B','E'):
                item['material'].count =F('count') +item['count']
            elif validated_data['type']=='O':
                item['material'].count =F('count') -item['count']
            item['material'].save()
            price=None
            if validated_data['type'] in ('B','O'):
                price=item['material'].price
            elif validated_data['type']=='E':
                price=item['material'].buyPrice
                
            InvoiceItem.objects.create(invoice=invoice,material=item['material'],price=price,count=item['count'])
        return invoice
    class Meta:
        model=Invoice 
        fields=['id','employee','employeeName','items','datetime','type','count']

class InvoiceItemSerializer(ModelSerializer):
    employeeName=CharField(source='invoice.employee.__str__',read_only=True)
    materialName=StringRelatedField(source='material')
    type=CharField(source='invoice.type') 
    datetime=DateTimeField(source='invoice.datetime')
    totalCount=IntegerField()
    
    class Meta:
        model=InvoiceItem
        fields=['price','count','invoice','employeeName','materialName','totalCount','datetime','type']
