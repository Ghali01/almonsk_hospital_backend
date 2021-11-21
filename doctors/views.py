from rest_framework.views import APIView, Response
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin,UpdateModelMixin,DestroyModelMixin
from .serializers import DoctorSerialzer
from .models import Doctor
from rest_framework.exceptions import MethodNotAllowed
from django.db.models.query_utils import Q
from patients.models import PatientConsult,PatientSurgery
from rest_framework.decorators import  api_view
class Doctors(GenericAPIView,CreateModelMixin,UpdateModelMixin,DestroyModelMixin):
    serializer_class=DoctorSerialzer
    queryset=Doctor.objects.all()
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    def put(self,request,pk=None,*args,**kwargs):
        return self.update(request,pk,*args,**kwargs)
    def delete(self,request,pk=None,*args,**kwargs):

        return self.destroy(request,pk,*args,**kwargs)
class DoctorsList(APIView):
    
    def get(self,request,*args,**kwargs):
        data=[]
        qSet=Doctor.objects.filter(Q(firstName__icontains=request.GET['search'])|Q(fatherName__icontains=request.GET['search'])|Q(secondName__icontains=request.GET['search'])) if 'search' in request.GET else Doctor.objects.all()
        for doctor  in qSet:
            account=0
            for cons in PatientConsult.objects.filter(doctor=doctor,paided=False):
                account+=cons.cost
            for surgery in PatientSurgery.objects.filter(Q(Q(surgeon=doctor,surgeonPaided=False)|Q(assistant=doctor,assistantPaided=False)|Q(anesthetic=doctor,anestheticPaided=False))):
                if surgery.surgeon and surgery.surgeon==doctor  and surgery.surgeonPaided==False  and surgery.surgeonCosts:
                    account+=surgery.surgeonCosts
                if surgery.assistant and surgery.assistant==doctor and surgery.assistantPaided==False  and surgery.assistantCosts:
                    account+=surgery.assistantCosts
                if  surgery.anesthetic and surgery.anesthetic==doctor and surgery.anestheticPaided==False  and surgery.anestheticCosts:
                    account+=surgery.anestheticCosts

            data.append({ 
                'id':doctor.id,
                'firstName':doctor.firstName,
                'secondName':doctor.secondName,
                'fatherName':doctor.fatherName,
                'phone':doctor.phone,
                'account': account
            })
        return Response(data=data)

class DoctorCosts(APIView):

    def get(self,request,id):
        data={}
        consults=[]
        surgeries=[]
        for cons in PatientConsult.objects.filter(doctor_id=id).order_by('paided')[:20]:
            consults.append({
                'id':cons.id,
                'patient':str(cons.patient) if cons.patient else None,
                'cost':cons.cost,
                'paided':cons.paided,
            })
        data['consults']=consults

        for surgery in PatientSurgery.objects.filter(Q(Q(surgeon_id=id)|Q(assistant_id=id)|Q(anesthetic_id=id)))[:20]:
            if surgery.surgeon and surgery.surgeon.id==id:
                surgeries.append({
                'id':surgery.id,
                'surgery':surgery.surgery.name,
                'patient':str(surgery.patient) if surgery.patient else None,
                'cost':surgery.surgeonCosts,
                'paided':surgery.surgeonPaided,
                'role':'S'
            }) 
            if surgery.assistant and surgery.assistant.id==id:
                surgeries.append({
                'id':surgery.id,
                'surgery':surgery.surgery.name,
                'patient':str(surgery.patient) if surgery.patient else None,
                'cost':surgery.assistantCosts,
                'paided':surgery.assistantPaided,
                'role':'AS'
            })    
            if  surgery.anesthetic and  surgery.anesthetic.id==id:
                surgeries.append({
                'id':surgery.id,
                'surgery':surgery.surgery.name,
                'patient':str(surgery.patient) if surgery.patient else None,
                'cost':surgery.anestheticCosts,
                'paided':surgery.anestheticPaided,
                'role':'AC'
            }) 
        surgeries.sort(key=lambda it:it['paided']==False ,reverse=True)
        data['surgeries']=surgeries
        consultsCount=0
        surgeriesCount=0
        for cons in PatientConsult.objects.filter(doctor_id=id,paided=False):
            consultsCount+=cons.cost
        for surgery in PatientSurgery.objects.filter(Q(Q(surgeon_id=id,surgeonPaided=False)|Q(assistant_id=id,assistantPaided=False)|Q(anesthetic_id=id,anestheticPaided=False))):
            if surgery.surgeonCosts and surgery.surgeon and surgery.surgeonPaided==False and surgery.surgeon.id==id:
                surgeriesCount+=surgery.surgeonCosts
            if surgery.assistantCosts and surgery.assistant and surgery.assistantPaided==False and surgery.anestheticPaided==False and surgery.assistant.id==id:
                surgeriesCount+=surgery.assistantCosts
            if  surgery.anestheticCosts and  surgery.anesthetic and surgery.anestheticPaided==False and  surgery.anesthetic.id==id:
                surgeriesCount+=surgery.anestheticCosts
        data['surgeriesCount']=surgeriesCount
        data['consultsCount']=consultsCount
        return Response(data=data)  
            
    def put(self,request,*args,**kwargs):
        surgeries=request.data['surgeries']
        for sur in surgeries:                        
            surgery=get_object_or_404(PatientSurgery,pk=int(sur['id']))
            if sur['role']=='S':
                surgery.surgeonPaided=True
            elif sur['role']=='AS':
                surgery.assistantPaided=True
            elif sur['role']=='AC':
                surgery.anestheticPaided=True

            surgery.save()
        consults=request.data['consults']
        PatientConsult.objects.filter(id__in=consults).update(paided=True)
       
        return Response('done')



class DoctorConsults(APIView):


    def get(self,request,id,page):
        consults=[]
        for cons in PatientConsult.objects.filter(doctor_id=id).order_by('paided')[20*(page-1):20*page]:
            consults.append({
                'id':cons.id,
                'patient':str(cons.patient) if cons.patient else None,
                'cost':cons.cost,
                'paided':cons.paided,
            })
        
        return Response(data=consults)
    
class DoctorSurgeries(APIView):


    def get(self,request,id,page):
      
        surgeries=[]
        
        for surgery in PatientSurgery.objects.filter(Q(Q(surgeon_id=id)|Q(assistant_id=id)|Q(anesthetic_id=id)))[10*(page-1):10*page]:
            if surgery.surgeon and surgery.surgeon.id==id:
                surgeries.append({
                'id':surgery.id,
                'surgery':surgery.surgery.name,
                'patient':str(surgery.patient) if surgery.patient else None,
                'cost':surgery.surgeonCosts,
                'paided':surgery.surgeonPaided,
                'role':'S'
            }) 
            if surgery.assistant and surgery.assistant.id==id:
                surgeries.append({
                'id':surgery.id,
                'surgery':surgery.surgery.name,
                'patient':str(surgery.patient) if surgery.patient else None,
                'cost':surgery.assistantCosts,
                'paided':surgery.assistantPaided,
                'role':'AS'
            })    
            if  surgery.anesthetic and  surgery.anesthetic.id==id:
                surgeries.append({
                'id':surgery.id,
                'surgery':surgery.surgery.name,
                'patient':str(surgery.patient) if surgery.patient else None,
                'cost':surgery.anestheticCosts,
                'paided':surgery.anestheticPaided,
                'role':'AC'
            }) 
        surgeries.sort(key=lambda it:it['paided']==False,reverse=True)

        return Response(data=surgeries)

@api_view(['PUT'])
def setSurgeryPaided(request):
    
    surgery=get_object_or_404(PatientSurgery,pk=int(request.data['id']))
    if request.data['role']=='S':
        surgery.surgeonPaided=True
        surgery.save()
    elif request.data['role']=='AS':
        surgery.assistantPaided=True
        surgery.save()
    elif request.data['role']=='AC':
        surgery.anestheticPaided=True
        surgery.save()

    return Response('done')

@api_view(['PUT'])
def setConsultPaided(request,id):
    cons=get_object_or_404(PatientConsult,pk=id) 
    cons.paided=True 
    cons.save()
    return Response('done')
