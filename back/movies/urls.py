from django.urls import path
from . import views


app_name = 'movies'
urlpatterns = [
    # 영화 정보
    path('', views.movie_list),
    path('<int:movie_pk>/', views.movie_detail),
    path('random', views.movie_random),
    path('<int:movie_pk>/like', views.like_movie),
    path('<int:movie_pk>/dislike', views.dislike_movie),
    path('<int:user_pk>/user_like_movie', views.user_like_movie),
    path('<int:user_pk>/user_dislike_movie', views.user_dislike_movie),
    path('<int:user_pk>/user_filtered_movie', views.user_filtered_movie_recommendations),
    path('<str:movie_name>/', views.search_movie),

    # 리뷰
    path('<int:movie_pk>/reviews/', views.reviews),
    path('<int:movie_pk>/create_review/', views.create_review),
    path('<int:movie_pk>/delete_review/', views.delete_review),

    # 추천
    path('recommended/', views.recommended),

    # 배우
    path('actors/<int:actor_pk>/', views.actor_detail),
    path('actors/<str:actor_name>/', views.search_actors),
]