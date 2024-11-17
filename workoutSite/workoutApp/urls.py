from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('exercises/', views.exerciseList, name='exerciseList'),
    path('add-to-routine/', views.add_to_routine, name='add_to_routine'),
    path('view-routine/', views.view_routine, name='view_routine'),
]