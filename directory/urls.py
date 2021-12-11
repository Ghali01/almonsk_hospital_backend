from django.urls import path
from directory.views import *
urlpatterns=[
    path('<int:page>',Materials.as_view(),name='materials'),
    path('',Materials.as_view(),name='materials'),
    path('employees',Employees.as_view(),name='employees'),
    path('invoices/<int:page>',Invoices.as_view(),name='invoices'),
    path('invoice-single/<int:pk>',InvoiceView.as_view(),name='invoice'),
    path('invoice-single',InvoiceView.as_view(),name='invoice'),
    path('material-invoices/<int:id>/<int:page>',InvovoiceItemOfMaterial.as_view(),name='material-invoices'),
    path('inventory-material/<int:id>/<int:year>',InventoryMaterial.as_view(),name='inventory-material'),
    path('inventory-employees-material/<int:id>/<int:year>/<int:month>',InventoryEmployeesOfMaterial.as_view(),name='inventory-employees-material'),
    path('inventory-employee-material/<int:employeeID>/<int:materialID>/<int:year>',InventoryMaterialEmployee.as_view(),name='inventory-employee-material')
]