from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.fields import IntegerField,CharField,DateTimeField
from rest_framework.relations import StringRelatedField
from .models import Drug,Employee, Invoice, InvoiceItem
from django.db.models import F

class DrugSerializer(ModelSerializer):
    class Meta:
        model=Drug
        fields=['id','name','price','buyPrice','count']
        read_only_fields=['id','count']

class UpdateDrugSerializer(ModelSerializer):
    class Meta:
        model=Drug
        fields=['id','name','price','buyPrice','count']
        # fields=['id','name','price','buyPrice','count']
        read_only_fields=['id','count','name']

        
class EmployeeSerializer(ModelSerializer):

    class Meta:
        model=Employee
        fields=['id','firstName','fatherName','secondName','inPermission','outPermission','phone']
class UpdateEmployeeSerializer(ModelSerializer):

    class Meta:
        model=Employee
        fields=['id','firstName','fatherName','secondName','inPermission','outPermission','phone']
        read_only_fields=['id','firstName','fatherName','secondName']


class InvoiceItemInInvoicSerializer(ModelSerializer):
    drugName= CharField(source='drug.name',read_only=True)
    price=IntegerField(read_only=True)
    class Meta:
        model=InvoiceItem
        fields=['drug','drugName','price','count']


class InvoiceListSerializer(ModelSerializer):
    employeeName=CharField(source='employee.__str__',read_only=True)
    count =IntegerField()
    class Meta:
        model=Invoice 
        fields=['id','employee','employeeName','datetime','type','count']

class InvoiceSerializer(ModelSerializer):
    items=InvoiceItemInInvoicSerializer(many=True)
    employeeName=CharField(source='employee.__str__',read_only=True)
    count =IntegerField(read_only=True)
    def create(self, validated_data):
        invoice=Invoice.objects.create(employee=validated_data['employee'],type=validated_data['type'])
        for item in validated_data['items']:
            if validated_data['type'] in ('B','E'):
                item['drug'].count =F('count') +item['count']
            elif validated_data['type']=='O':
                item['drug'].count =F('count') -item['count']
            item['drug'].save()
            price=None
            if validated_data['type'] in ('B','O'):
                price=item['drug'].price
            elif validated_data['type']=='E':
                price=item['drug'].buyPrice
                
            InvoiceItem.objects.create(invoice=invoice,drug=item['drug'],price=price,count=item['count'])
        return invoice
    class Meta:
        model=Invoice 
        fields=['id','employee','employeeName','items','datetime','type','count']

class InvoiceItemSerializer(ModelSerializer):
    employeeName=CharField(source='invoice.employee.__str__',read_only=True)
    drugName=StringRelatedField(source='drug')
    type=CharField(source='invoice.type') 
    datetime=DateTimeField(source='invoice.datetime')
    totalCount=IntegerField()
    
    class Meta:
        model=InvoiceItem
        fields=['price','count','invoice','employeeName','drugName','totalCount','datetime','type']
