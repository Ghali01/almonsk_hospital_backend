from rest_framework.views import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin,UpdateModelMixin,DestroyModelMixin
from .serializers import DoctorSerialzer
from .models import Doctor
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import MethodNotAllowed
from django.db.models.query_utils import Q
class Doctors(GenericAPIView,CreateModelMixin,UpdateModelMixin,DestroyModelMixin):
    serializer_class=DoctorSerialzer
    queryset=Doctor.objects.all()
    
    def get(self,request,*args,**kwargs):
        data=[]
        qSet=self.get_queryset().filter(Q(firstName__icontains=request.GET['search'])|Q(fatherName__icontains=request.GET['search'])|Q(secondName__icontains=request.GET['search'])) if 'search' in request.GET else self.get_queryset()
        for doctor  in qSet:
            data.append({ 
                'id':doctor.id,
                'firstName':doctor.firstName,
                'secondName':doctor.secondName,
                'fatherName':doctor.fatherName,
                'phone':doctor.phone,
                'account':0
            })
        return Response(data)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    def put(self,request,pk=None,*args,**kwargs):
        if not pk:
            raise MethodNotAllowed(detail="ID is required",method=['PUT'])
        return self.update(request,pk,*args,**kwargs)
    def delete(self,request,pk=None,*args,**kwargs):
        if not pk:
            raise MethodNotAllowed(detail="ID is required",method=['PUT'])

        return self.destroy(request,pk,*args,**kwargs)