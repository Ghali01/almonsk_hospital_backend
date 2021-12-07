from rest_framework.serializers import ModelSerializer
from .models import Surgery


class SurgerySerializer(ModelSerializer):
    class Meta:
        model=Surgery
        fields=['id','name','duration','price']