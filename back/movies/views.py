from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import (
    MovieListSerializer,
    ReviewSerializer,
    MovieSerializer,
    ActorSerializer,
)
from .models import Movie, Review, Actor

# 모든 영화
@api_view(['GET'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        paginator = Paginator(movies, 20)

        page = request.GET.get('page', 1)
        page_movies = paginator.get_page(page)

        serializer = MovieListSerializer(page_movies, many=True)
        return Response(serializer.data)
    
# 각 영화별 디테일 정보
@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializr = MovieSerializer(movie)
    return Response(serializr.data)

@api_view(['GET'])
def recommended(request):
    pass

# 리뷰 목록
@api_view(['GET'])
def reviews(request, movie_pk):
    if request.method == 'GET':
        reviews = Review.objects.all().filter(movie_id=movie_pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

# 리뷰 생성
@api_view(['POST'])
def create_review(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=user)
        reviews = movie.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 리뷰 삭제
@api_view(['DELETE'])
def delete_review(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if request.user == review.user:
        review.delete()
        movie = get_object_or_404(Movie, pk=movie_pk)
        reviews = movie.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

# 배우 디테일
@api_view(['GET'])
def actor_detail(request, actor_pk):
    actor = get_object_or_404(Actor, pk=actor_pk)
    serializer = ActorSerializer(actor)
    return Response(serializer.data)

# 영화 좋아요
@api_view(['POST'])
def like_movie(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    else:
        if movie.dislike_users.filter(pk=user.pk).exists():
            movie.dislike_users.remove(user)
        movie.like_users.add(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
# 영화 싫어요
@api_view(['POST'])
def like_movie(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.dislike_users.filter(pk=user.pk).exists():
        movie.dislike_users.remove(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    else:
        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user)
        movie.dislike_users.add(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)