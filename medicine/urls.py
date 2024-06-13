from . import views
from django.urls import path

urlpatterns = [
        path('add/',views.add_medicine,name='addmedicine'),
         path('medicine_list/',views.medicine_list,name='medicinelist'),
         path('update/<int:pk>/',views.update_medicine,name='updatemedicine'),
         path('delete/<int:pk>',views.delete_medicine,name='deletemedicine'),
         path('search/', views.search_medicine, name='search_medicine'),

]
