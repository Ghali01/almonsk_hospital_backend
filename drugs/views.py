from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from .serializers import Drug,DrugSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
class Drugs(GenericAPIView,ListModelMixin,CreateModelMixin):
    serializer_class=DrugSerializer
    queryset=Drug.objects.all()
    
    def filter_queryset(self, queryset):
        if self.request.method=='GET' and 'search' in self.request.GET :
            page=self.kwargs['page']
            if self.request.GET['search']:
                print(self.request.GET['search'])
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
            surgery=Drug.objects.get(pk=request.data['id'])
            serializered=DrugSerializer(instance=surgery,data=request.data)
            if serializered.is_valid():
                serializered.save()

            return Response(serializered.data)
        raise ValidationError(detail='id is required')
       