from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from .serializers import Surgery,SurgerySerializer
from rest_framework.exceptions import ValidationError
class Surgeries(GenericAPIView,ListModelMixin,CreateModelMixin):
    serializer_class=SurgerySerializer
    queryset=Surgery.objects.all()

    
    def filter_queryset(self, queryset):
        if self.request.method=='GET' and 'search' in self.request.GET:
            page=self.kwargs['page']
            if self.request.GET['search']:
                return queryset.filter(name__icontains=self.request.GET['search'])[20*(page-1):20*page]
            return queryset[20*(page-1):20*page]
                
        return queryset

    def get(self,request,*args,**kwargs):
        return self.list(request)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    def put(self,request,*args,**kwargs):
        if  'id' in request.data:
            surgery=Surgery.objects.get(pk=request.data['id'])
            serializered=SurgerySerializer(instance=surgery,data=request.data)
            if serializered.is_valid():
                serializered.save()

            return Response(serializered.data)
        raise ValidationError(detail='id is required')
       