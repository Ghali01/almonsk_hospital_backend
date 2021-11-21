from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin,CreateModelMixin,DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from .serializers import *
class Patients(GenericAPIView,ListModelMixin,RetrieveModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin):
    filter_backends=[SearchFilter]
    search_fields=['firstName','fatherName','secondName','acceptID']
    lookup_url_kwarg='prami'    
    queryset=Patient.objects.all()
    LIST='list'
    ACCEPT='accept'


    def get_serializer_class(self):
        
        if self.kwargs['mode']==self.LIST:
            return PatientListSerializer
        elif self.kwargs['mode']==self.ACCEPT:
            return PatientAcceptSerializer
    def filter_queryset(self, queryset):
        queryset= super().filter_queryset(queryset)
        if self.kwargs['mode']==self.LIST and  self.request.method=='GET' :
            page=self.kwargs['prami']
            queryset= queryset[10*(page-1):page*10]
        
        return queryset
    def get(self,request,*args,**kwargs):
        if  self.kwargs['mode']==self.LIST:
          return self.list(request)  
        else: 
            return self.retrieve(request)

    def post(self,request,*args,**kwargs):
        if  self.kwargs['mode']==self.ACCEPT:
            return self.create(request)
        else:
            raise MethodNotAllowed('POST')
    def put(self,request,*args,**kwargs):
      return self.update(request)

    def delete(self,request,*args,**kwargs):
        if self.kwargs['mode']==self.ACCEPT:
            return self.destroy(request)
        else:
            raise MethodNotAllowed('DELETE')

class PatientsList(GenericAPIView,ListModelMixin):
    serializer_class=PatientListSerializer
    queryset=Patient.objects.all()
    def filter_queryset(self, queryset):
        queryset= super().filter_queryset(queryset)
        page=self.kwargs['page']
        queryset= queryset[10*(page-1):page*10]
        
        return queryset
    def get(self,request,*args,**kwargs):
          return self.list(request)  

class PatientAccept(GenericAPIView,RetrieveModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin):
    serializer_class=PatientAcceptSerializer
    queryset=Patient.objects.all()
    def get(self,request,*args,**kwargs):
      return self.retrieve(request)

    def post(self,request,*args,**kwargs):
        return self.create(request)
    def put(self,request,*args,**kwargs):
      return self.update(request)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request)

class PatientCosts(APIView):


    def get(self,request,id):
        costs=patientCosts.objects.get(patient_id=id) 
        consults=PatientConsult.objects.filter(patient_id=id)
        serializerdCosts=PatientCostSerializer(instance=costs,data={})
        serializerdCosts.is_valid()
        seriailzerdConsults=ConsultSerializer(consults,many=True)
        return Response(data={'costs':PatientCostSerializer(instance=costs).data,'consults':seriailzerdConsults.data})
    def put(self,request,id):
        patient_Costs=patientCosts.objects.get(patient_id=id)
        seriailzerdCosts=PatientCostSerializer(instance=patient_Costs,data=request.data['costs'])
        if seriailzerdCosts.is_valid():
            seriailzerdCosts.save()
        PatientConsult.objects.filter(patient_id=id,paided=False).delete()
        for e in request.data['consults']:
            e['patient']=id
        
        seriailzerdConsults=ConsultSerializer(data=request.data['consults'],many=True)
        seriailzerdConsults.is_valid()
        seriailzerdConsults.save()
        return Response(data={
            'costs':seriailzerdCosts.data,
            'consults':seriailzerdConsults.data
            })



class PatientDrugs(GenericAPIView,ListModelMixin):
    serializer_class=PatientDrugSerializer


    def get_queryset(self):
        return PatientDrug.objects.filter(patient_id=self.kwargs['id'])

    def get(self,request,*args,**kwargs):
        return self.list(request)

    def put(self,request,*args,**kwargs):
        PatientDrug.objects.filter(patient_id=self.kwargs['id']).delete()
        serializered=PatientDrugSerializer(data=request.data,many=True)
        if serializered.is_valid():
            serializered.save()
        return Response(data=serializered.data)

class PatientSurgeries(GenericAPIView,ListModelMixin):
    serializer_class=PatienSurgerySerializer


    def get_queryset(self):
        query_set=PatientSurgery.objects.filter(patient_id=self.kwargs['id'])
        return query_set

    def get(self,request,*args,**kwargs):
        return self.list(request)

    def put(self,request,*args,**kwargs):
        ids=[]
        for surgery in request.data:
            serializered=None
            if 'id' in surgery and not surgery['id']== None:
                surgeryObj =PatientSurgery.objects.get(pk=int(surgery['id']))
                serializered=PatienSurgerySerializer(instance=surgeryObj,data=surgery)
            else:
                serializered=PatienSurgerySerializer(data=surgery)

            if serializered.is_valid():
                serializered.save()
                ids.append(serializered.data['id'])
 
        PatientSurgery.objects.filter(patient_id=self.kwargs['id']).exclude(id__in=ids).delete()
        return Response(serializered.data)

class Invoice(APIView):
    def get(self,request,id,*args,**kwargs):
        patient=Patient.objects.get(pk=id)
        drugsCount=0
        for drug in patient.drugs.all():
            drugsCount+=drug.price*drug.count
        serilaizered=InvoiceSerializer(instance=patient)
        # serilaizered.is_valid()
        data=dict(serilaizered.data)
        data['ECGAndEcho']= (patient.costs.ECG if patient.costs.ECG else 0)+(patient.costs.echo if patient.costs.echo else 0)
        data['raysAndAxial']=(patient.costs.rays if patient.costs.rays else 0)+(patient.costs.axial if patient.costs.axial else 0)
        data['drugsCount']=drugsCount
        
        return Response(data)