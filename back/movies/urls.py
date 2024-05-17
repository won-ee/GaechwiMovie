from django.urls import path
from . import views


app_name = 'movies'
urlpatterns = [
    # 영화 정보
    path('', views.movie_list),
    path('<int:movie_pk>/', views.movie_detail),

    # 리뷰
    path('<int:movie_pk>/reviews/', views.reviews),
    path('<int:movie_pk>/create_review/', views.create_review),
    path('<int:movie_pk>/delete_review/', views.delete_review),

    # 추천
    path('recommended/', views.recommended),

    # 배우
    path('actors/<int:actor_pk>/', views.actor_detail),
]