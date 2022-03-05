from django.db import models
class Surgery(models.Model):
    name=models.CharField(max_length=100)
    price=models.PositiveIntegerField()
    duration =models.FloatField()
    QHAP=models.PositiveBigIntegerField()
    class Meta:
        ordering=['name']