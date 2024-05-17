from django.urls import path
from . import views


app_name = 'movies'
urlpatterns = [
    path('', views.movie_list),
    path('<int:movie_pk>/', views.movie_detail),
    path('<int:movie_pk>/reviews/', views.reviews),
    path('<int:movie_pk>/create_review/', views.create_review),
    path('<int:movie_pk>/delete_review/', views.delete_review),
    path('recommended/', views.recommended),
]