from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from .serializers import Surgery,SurgerySerializer

class Surgeries(GenericAPIView,ListModelMixin):
    serializer_class=SurgerySerializer
    queryset=Surgery.objects.all()

    def get(self,request):
        return self.list(request)

    def put(self,request):
        for item in request.data:
            serializerd=SurgerySerializer(self.get_queryset().get(pk=item['id']),item) if 'id' in item else SurgerySerializer(data=item)
            if serializerd.is_valid():
                serializerd.save()
        return self.list(request)