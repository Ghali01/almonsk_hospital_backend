from rest_framework.serializers import ModelSerializer
from .models import Drug


class DrugSerializer(ModelSerializer):


    class Meta:
        model=Drug
        fields=['id','name','price']