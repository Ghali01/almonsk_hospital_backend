from rest_framework.serializers import ModelSerializer
from rest_framework.fields import IntegerField
from .models import Surgery


class SurgerySerializer(ModelSerializer):
    QHAP=IntegerField(required=False,allow_null=True)
    class Meta:
        model=Surgery
        fields='__all__'

    def create(self, data):
        if not 'QHAP' in data or ('QHAP' in data and not data['QHAP']):
            data['QHAP']=data['price']/4 
        return super().create(data)
    def update(self,obj, data):
        if not 'QHAP' in data or ('QHAP' in data and not data['QHAP']):
            data['QHAP']=data['price']/4 
        
        return super().update(obj,data)
        