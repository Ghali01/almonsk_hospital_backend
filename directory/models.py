from django.db import models


class Material(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    count=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name
    

    class Meta:
        ordering=['name']

class Employee(models.Model):
    firstName=models.CharField(max_length=50)
    fatherName=models.CharField(max_length=50)
    secondName=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)

    def __str__(self) :
        return f'{self.firstName} {self.fatherName} {self.secondName}'
    class Meta:
        ordering=['firstName','fatherName','secondName']
class Invoice(models.Model):
    typeChoices=[ 
        ('O','Out'),
        ('E','Enter'),
        ('B','Back'),
    ]
    type=models.CharField(max_length=1,choices=typeChoices)
    employee=models.ForeignKey(Employee,null=True,on_delete=models.SET_NULL)
    datetime=models.DateTimeField(auto_now_add=True)
    
    def count(self):
        count=0
        for item  in self.items.all():
            count+=item.count*item.price  
        return count
    class Meta:
        ordering=['-datetime']
    class Types:
        Enter='E'
        Out='O'
        Back='B'
class InvoiceItem(models.Model):
    material=models.ForeignKey(Material,on_delete=models.CASCADE)
    invoice=models.ForeignKey(Invoice,on_delete= models.CASCADE,related_name='items')
    count=models.PositiveIntegerField()
    price=models.PositiveIntegerField()
    
    def totalCount(self):
        return self.price*self.count

    class Meta:
        ordering=['-invoice__datetime']