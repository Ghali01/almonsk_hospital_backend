from rest_framework import serializers
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
        else:
            print('s')
        PatientConsult.objects.filter(patient_id=id).delete()
        for e in request.data['consults']:
            e['patient']=id
        
        seriailzerdConsults=ConsultSerializer(data=request.data['consults'],many=True)
        seriailzerdConsults.is_valid()
        seriailzerdConsults.save()
        return Response(data={
            'costs':seriailzerdCosts.data,
            'consults':seriailzerdConsults.data
            })