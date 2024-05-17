from django.urls import path
from . import views


app_name = 'profile'
urlpatterns = [
    path('profile/<str:nickname>/', views.profile),
    
]
