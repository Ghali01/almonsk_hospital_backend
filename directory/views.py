from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin, RetrieveModelMixin, UpdateModelMixin

from directory.models import Employee, Invoice, InvoiceItem
from .serializers import Material,MaterialSerializer, EmployeeSerializer, InvoiceItemSerializer, InvoiceListSerializer, InvoiceSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.db.models import F,Value,CharField,Q,Sum
from django.db.models.functions import Concat 
class Materials(GenericAPIView,ListModelMixin,CreateModelMixin):
    serializer_class=MaterialSerializer
    queryset=Material.objects.all()
    
    def filter_queryset(self, queryset):
        if self.request.method=='GET' and 'search' in self.request.GET :
            page=self.kwargs['page']
            if self.request.GET['search']:
                q=queryset.filter(name__icontains=self.request.GET['search'])[20*(page-1):20*page]
                return q 
            
            return queryset[20*(page-1):20*page]
            
        return queryset
    def get(self,request,*args,**kwargs):

        return self.list(request)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    def put(self,request,*args,**kwargs):
        if  'id' in request.data:
            surgery=Material.objects.get(pk=request.data['id'])
            serializered=MaterialSerializer(instance=surgery,data=request.data)
            if serializered.is_valid():
                serializered.save()

            return Response(serializered.data)
        raise ValidationError(detail='id is required')

class Employees(GenericAPIView,ListModelMixin,UpdateModelMixin,CreateModelMixin):
    serializer_class=EmployeeSerializer
    queryset=Employee.objects.all()

    def filter_queryset(self, queryset):
        queryset= self.get_queryset()
        if self.request.method=='GET'  and 'search' in self.request.GET:
            queryset=queryset.annotate(fullName=Concat(F('firstName'),Value(' '),F('fatherName'),Value(' '),F('secondName'),output_field=CharField()),
                                    fsName=Concat(F('firstName'),Value(' '),F('secondName'),output_field=CharField()))
            queryset=queryset.filter(Q(fullName__istartswith=self.request.GET['search'])|Q(fsName__istartswith=self.request.GET['search']))
        if 'permission' in self.request.GET and self.request.GET['permission'] in ('in','out'):
            queryset=queryset.filter(**{self.request.GET['permission']+'Permission':True})

            
        return queryset
    def get(self,request):
        return self.list(request)

    def post(self,request): 
        return self.create(request)
    def put(self,request,*args,**kwargs):
        return self.update(request)
class Invoices(GenericAPIView,ListModelMixin):

    queryset=Invoice.objects.all()
    serializer_class=InvoiceListSerializer
    def filter_queryset(self, queryset):
        qSet=self.get_queryset()
        if 'date' in self.request.GET:
            year,month=self.request.GET['date'].split('-')
            qSet=qSet.filter(datetime__year=int(year),datetime__month=int(month))
        if 'employee' in self.request.GET:
            qSet=qSet.filter(employee_id=self.request.GET['employee'])
        if 'type' in self.request.GET:
            qSet=qSet.filter(type=self.request.GET['type'])  
        page=self.kwargs['page']
        return qSet[20*(page-1):20*page]
    def get(self,request,*args,**kwargs):
        return self.list(request)

class InvoiceView(GenericAPIView,RetrieveModelMixin,CreateModelMixin):

    queryset=Invoice.objects.all()
    serializer_class=InvoiceSerializer
    def get(self,request,pk=None,*args,**kwargs):
        if pk is None:
            raise ValidationError('id is required')
        return self.retrieve(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        
        return self.create(request)

class InvovoiceItemOfMaterial(GenericAPIView,ListModelMixin):

    serializer_class=InvoiceItemSerializer
    queryset=InvoiceItem.objects.all()

    def filter_queryset(self, queryset):
        qSet=self.get_queryset()
        qSet=qSet.filter(material_id=self.kwargs['id'])
        if 'date' in self.request.GET:
            year,month=self.request.GET['date'].split('-')
            qSet=qSet.filter(invoice__datetime__year=year,invoice__datetime__month=month)
        if 'employee' in self.request.GET:
            qSet=qSet.filter(invoice__employee_id=self.request.GET['employee'])
        if 'type' in self.request.GET:
            qSet=qSet.filter(invoice__type=self.request.GET['type'])
        pg=self.kwargs['page']
        return qSet[20*(pg-1):20*pg]
    
    def get(self,request,*args,**kwargs):
        return self.list(self,request)


class InventoryMaterial(APIView):

    def get(self,request,id,year):

        invoices=InvoiceItem.objects.filter(material_id=id,invoice__datetime__year=year)
        resault=[]
        for month in range(1,13):
            out=0
            enter=0
            back=0
            for item in invoices.filter(invoice__datetime__month=month,invoice__type=Invoice.Types.Out):
                out+=item.count 
            for item in invoices.filter(invoice__datetime__month=month,invoice__type=Invoice.Types.Enter):
                enter+=item.count 
            for item in invoices.filter(invoice__datetime__month=month,invoice__type=Invoice.Types.Back):
                back+=item.count 
            resault.append({'out':out,
                            'enter':enter,
                            'back':back
                            })
        return Response(resault)


class InventoryEmployeesOfMaterial(APIView):



    def get(self,request,id,year,month): 
        data=InvoiceItem.objects.filter(material_id=id,invoice__datetime__year=year,invoice__datetime__month=month) 
        data=data.values('invoice__employee','invoice__type').annotate(tCount=Sum('count')).order_by()
        employees=Employee.objects.all()
        
        resault=[]
        for emp in employees:
            empID=emp.id
            name=f'{emp.firstName} {emp.fatherName} {emp.secondName}'
            enter = data.filter(invoice__employee=empID,invoice__type=Invoice.Types.Enter)[0]['tCount'] if data.filter(invoice__employee=empID,invoice__type=Invoice.Types.Enter).exists() else 0
            out = data.filter(invoice__employee=empID,invoice__type=Invoice.Types.Out)[0]['tCount'] if data.filter(invoice__employee=empID,invoice__type=Invoice.Types.Out).exists() else 0
            back = data.filter(invoice__employee=empID,invoice__type=Invoice.Types.Back)[0]['tCount'] if data.filter(invoice__employee=empID,invoice__type=Invoice.Types.Back).exists() else 0
            if out or enter or back:
                resault.append({
                    'name':name,
                    'enter':enter,
                    'out':out,
                    'back':back,
                })
        return Response(resault)

class InventoryMaterialEmployee(APIView):

    def get(self,request,employeeID,materialID,year):
        invoices=InvoiceItem.objects.filter(invoice__datetime__year=year,invoice__employee_id=employeeID,material_id=materialID).values('invoice__datetime__month','invoice__type').annotate(tCount=Sum('count')).order_by()
        resault=[]
        for month in range(1,13):
            out =invoices.filter(invoice__datetime__month=month,invoice__type=Invoice.Types.Out)[0]['tCount'] if invoices.filter(invoice__datetime__month=month,invoice__type=Invoice.Types.Out).exists() else 0
            enter =invoices.filter(invoice__datetime__month=month,invoice__type=Invoice.Types.Enter)[0]['tCount'] if invoices.filter(invoice__datetime__month=month,invoice__type=Invoice.Types.Enter).exists() else 0
            back =invoices.filter(invoice__datetime__month=month,invoice__type=Invoice.Types.Back)[0]['tCount'] if invoices.filter(invoice__datetime__month=month,invoice__type=Invoice.Types.Back).exists() else 0
            
            resault.append({
                'out':out,
                'enter':enter,
                'back':back,
                'month':month
            })
        return Response(resault)