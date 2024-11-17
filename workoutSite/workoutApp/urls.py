from django.urls import path
from workoutApp import views
from django.http import HttpResponse

def placeholder_view(request):
    return HttpResponse("This page is under construction.")


urlpatterns = [
    path('', views.home, name='home'),
    path('exercises/', views.exerciseList, name='exerciseList'),
    path('add-to-routine/', views.add_to_routine, name='add_to_routine'),
    path('view-routine/', views.view_routine, name='view_routine'),
    path('profile/', placeholder_view, name='profile'),
]