from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from .serializers import Drug,DrugSerializer

class Drugs(GenericAPIView,ListModelMixin):
    serializer_class=DrugSerializer
    queryset=Drug.objects.all()
    
    def filter_queryset(self, queryset):
        if self.request.method=='GET' and 'search' in self.request.GET :
            page=self.kwargs['page']
            if self.request.GET['search']:
                print(self.request.GET['search'])
                q=queryset.filter(name__icontains=self.request.GET['search'])[10*(page-1):10*page]
                print(q )
                return q 
            
            return queryset[10*(page-1):10*page]
            
        return queryset
    def get(self,request,*args,**kwargs):

        return self.list(request)

    def put(self,request,*args,**kwargs):
        for item in request.data:
            serializerd=DrugSerializer(self.get_queryset().get(pk=item['id']),item) if 'id' in item else DrugSerializer(data=item)
            if serializerd.is_valid():
                serializerd.save()
        return self.list(request)