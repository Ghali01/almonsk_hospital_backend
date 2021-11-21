from django.urls import path
from patients import views 
urlpatterns=[ 
    path('costs/<int:id>',views.PatientCosts.as_view(),name='patient-costs'),
    path('drugs/<int:id>',views.PatientDrugs.as_view(),name='patient-drugs'),
    path('surgeries/<int:id>',views.PatientSurgeries.as_view(),name='patient-drugs'),
    path('invoice/<int:id>',views.Invoice.as_view(),name='patient-drugs'),
    path('list/<int:page>',views.PatientsList.as_view(),name='patients-list'),
    path('accept',views.PatientAccept.as_view(),name='patients-accept'),
    path('accept/<int:pk>',views.PatientAccept.as_view(),name='patients-accept'),
]