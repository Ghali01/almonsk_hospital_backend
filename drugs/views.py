from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from .serializers import Drug,DrugSerializer

class Drugs(GenericAPIView,ListModelMixin):
    serializer_class=DrugSerializer
    queryset=Drug.objects.all()

    def get(self,request):
        return self.list(request)

    def put(self,request):
        for item in request.data:
            serializerd=DrugSerializer(self.get_queryset().get(pk=item['id']),item) if 'id' in item else DrugSerializer(data=item)
            if serializerd.is_valid():
                serializerd.save()
        return self.list(request)