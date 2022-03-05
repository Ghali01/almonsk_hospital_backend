from datetime import datetime
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin,CreateModelMixin,DestroyModelMixin
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError 
from .serializers import *
import re 
from django.db.models import F,CharField,Value,Q
from django.db.models.functions import Concat


class PatientsList(GenericAPIView,ListModelMixin):
    serializer_class=PatientListSerializer
    queryset=Patient.objects.all()
    def filter_queryset(self, queryset):
        queryset= self.get_queryset()
        if 'search' in self.request.GET:
            if self.request.GET['search'].isdigit():
                print('id')
                queryset=queryset.filter(acceptID=int(self.request.GET['search']))
            else:
                queryset=queryset.annotate(fullName=Concat(F('firstName'),Value(' '),F('fatherName'),Value(' '),F('secondName'),output_field=CharField()),
                                            fsName=Concat(F('firstName'),Value(' '),F('secondName'),output_field=CharField()))
                queryset=queryset.filter(Q(fullName__istartswith=self.request.GET['search'])|Q(fsName__istartswith=self.request.GET['search']))
            
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
        serializered=None
        for surgery in request.data:
            if 'id' in surgery and not surgery['id']== None:
                surgeryObj =PatientSurgery.objects.get(pk=int(surgery['id']))
                serializered=PatienSurgerySerializer(instance=surgeryObj,data=surgery)
            else:
                serializered=PatienSurgerySerializer(data=surgery)

            if serializered.is_valid():
                serializered.save()
                ids.append(serializered.data['id'])
 
        PatientSurgery.objects.filter(patient_id=self.kwargs['id']).exclude(id__in=ids).delete()
        return Response(serializered.data if not serializered==None else '')

class Invoice(APIView):
    def get(self,request,id,*args,**kwargs):
        patient=Patient.objects.get(pk=id)
        serilaizered=InvoiceSerializer(instance=patient)
        data=dict(serilaizered.data)
        drugsCount=0
        for drug in patient.drugs.all():
            drugsCount+= (drug.price*drug.count if not drug.discrete else 0)
        data['drugsCount']=drugsCount
        data['ECGAndEcho']= (patient.costs.ECG if patient.costs.ECG else 0)+(patient.costs.echo if patient.costs.echo else 0)
        data['raysAndAxial']=(patient.costs.rays if patient.costs.rays else 0)+(patient.costs.axial if patient.costs.axial else 0)
        surgeries=PatientSurgery.objects.filter(patient=patient)
        doctorCosts=0
        assistantCosts=0
        anestheticCosts=0
        for surgery in surgeries:
            doctorCosts+=surgery.surgeonCosts or 0
            assistantCosts+=surgery.assistantCosts or 0
            anestheticCosts+=surgery.anestheticCosts or 0
        consults=PatientConsult.objects.filter(patient=patient)
        for cons in consults:
            assistantCosts+=cons.cost
        data['doctorCosts']=doctorCosts
        data['assistantCosts']=assistantCosts
        data['anestheticCosts']=anestheticCosts
        # print(data)
        return Response(data)

@api_view(['PUT'])
def lockPatientProfile(request,id):
    patient=get_object_or_404(Patient,pk=id)
    if 'outDate' in request.data and 'outTime' in request.data:
        patient.outDate=datetime.strptime(request.data['outDate'],'%Y-%m-%d').date() if  patient.outDate==None else patient.outDate
        patient.outTime=datetime.strptime(request.data['outTime'],'%H:%M').time() if  patient.outTime==None else patient.outTime
        patient.locked=True
        patient.save()
        return Response('done',200)
    else:
        raise ValidationError('out time and date are requrid')