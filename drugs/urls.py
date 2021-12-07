from django.urls import path
from .views import *
urlpatterns=[ 
    path('<int:page>',Drugs.as_view(),name='drugs'),
    path('',Drugs.as_view(),name='drugs'),
    path('employees',Employees.as_view(),name='employees'),
    path('invoices/<int:page>',Invoices.as_view(),name='invoices'),
    path('invoice-single/<int:pk>',InvoiceView.as_view(),name='invoice'),
    path('invoice-single',InvoiceView.as_view(),name='invoice'),
    path('drug-invoices/<int:id>/<int:page>',InvovoiceItemOfDrug.as_view(),name='drug-invoices'),
    path('inventory-drug/<int:id>/<int:year>',InventoryDrug.as_view(),name='inventory-drug'),
    path('inventory-employees-drug/<int:id>/<int:year>/<int:month>',InventoryEmployeesOfDrug.as_view(),name='inventory-employees-drug'),
    path('inventory-employee-drug/<int:employeeID>/<int:drugID>/<int:year>',InventoryDrugEmployee.as_view(),name='inventory-employee-drug')
]