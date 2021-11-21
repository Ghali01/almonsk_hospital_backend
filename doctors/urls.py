from django.urls import path
from doctors  import views
urlpatterns=[ 
    path('',views.Doctors.as_view(),name='doctors'),
    path('list',views.DoctorsList.as_view(),name='doctors'),
    path('<int:pk>',views.Doctors.as_view(),name='doctors'),
    path('costs/<int:id>',views.DoctorCosts.as_view(),name='doctors-costs'),
    path('consults/<int:id>/<int:page>',views.DoctorConsults.as_view(),name='doctor-consults'),
    path('surgeries/<int:id>/<int:page>',views.DoctorSurgeries.as_view(),name='doctor-surgeries'),
    path('surgery-paided',views.setSurgeryPaided,name='surgery-paided'),
    path('consult-paided/<int:id>',views.setConsultPaided,name='consult-paided'),
]
