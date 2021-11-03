from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from .serializers import Surgery,SurgerySerializer

class Surgeries(GenericAPIView,ListModelMixin):
    serializer_class=SurgerySerializer
    queryset=Surgery.objects.all()

    
    def filter_queryset(self, queryset):
        if self.request.method=='GET' and 'search' in self.request.GET:
            page=self.kwargs['page']
            if self.request.GET['search']:
                return queryset.filter(name__icontains=self.request.GET['search'])[10*(page-1):10*page]
            return queryset[10*(page-1):10*page]
                
        return queryset

    def get(self,request,*args,**kwargs):
        return self.list(request)

    def put(self,request,*args,**kwargs):
        for item in request.data:
            serializerd=SurgerySerializer(self.get_queryset().get(pk=item['id']),item) if 'id' in item else SurgerySerializer(data=item)
            if serializerd.is_valid():
                serializerd.save()
        return self.list(request)