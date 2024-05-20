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
    MovieSearchSerializer,
    UserLikeMovieListSerializer,
    UserDislikeMovieListSerializer,
    UserChoiceSimilarMovieSerializer,
    ActorSearchSerializer
)
from .models import Movie, Review, Actor
from accounts.models import User
import random

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from jellyfish import jaro_winkler_similarity

# 모든 영화 인기순
@api_view(['GET'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.filter(vote_count__gte=10000).order_by('-vote_average')
        paginator = Paginator(movies, 50)

        page = request.GET.get('page', 1)
        page_movies = paginator.get_page(page)

        serializer = MovieListSerializer(page_movies, many=True)
        return Response(serializer.data)

# 모든 영화 싫어요 순
@api_view(['GET'])
def movie_Worst_list(request):
    if request.method == 'GET':
        movies = Movie.objects.filter(vote_count__gte=10000).order_by('vote_average')
        paginator = Paginator(movies, 50)

        page = request.GET.get('page', 1)
        page_movies = paginator.get_page(page)

        serializer = MovieListSerializer(page_movies, many=True)
        return Response(serializer.data)

# 랜덤 영화
@api_view(['GET'])
def movie_random(request):
    movies = Movie.objects.filter(vote_count__gte=5000)
    random_movies = random.sample(list(movies), 1)
    
    serializer = MovieSerializer(random_movies, many=True)

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
def dislike_movie(request, movie_pk):
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
    
# 편집거리 알고리즘 - 영화
def search1(lst, keyword):
    fetch_data = []
    for data in lst:
        tmp = {'pk': 0, 'title': '', 'poster_path':'', 'similarity':''}
        tmp['pk'] = data['pk']; tmp['title'] = data['title']; tmp['poster_path'] = data['poster_path']
        tmp['similarity'] = jaro_winkler_similarity(keyword, data['title'])
        fetch_data.append(tmp)
    fetch_data.sort(key=lambda x : -x['similarity'])
    return fetch_data

# 편집거리 알고리즘 - 배우
def search2(lst, keyword):
    fetch_data = []
    for data in lst:
        tmp = {'pk': 0, 'name': '', 'profile_path':'', 'similarity':''}
        tmp['pk'] = data['pk']; tmp['name'] = data['name']; tmp['profile_path'] = data['profile_path']
        tmp['similarity'] = jaro_winkler_similarity(keyword, data['name'])
        fetch_data.append(tmp)
    fetch_data.sort(key=lambda x : -x['similarity'])
    return fetch_data

# 영화 제목 검색
@api_view(['GET'])
def search_movie(request, movie_name):
    movies = get_list_or_404(Movie)
    serializer = MovieSearchSerializer(movies, many=True)
    serializer = search1(serializer.data, movie_name)
    return Response(serializer[:6])

# 배우 이름 검색
@api_view(['GET'])
def search_actors(request, actor_name):
    actors = get_list_or_404(Actor)
    serializer = ActorSearchSerializer(actors, many=True)
    serializer = search2(serializer.data, actor_name)
    return Response(serializer[:6])

# 추천 알고리즘
def recommend_movies_names(xMovie, idx, movies):
    # None값과 빈 문자열을 제거
    xMovie = [text for text in xMovie if text is not None and text.strip() != '']
    # 유효한 데이터가 있는 지 확인
    if not xMovie:
        return []
    # 불용어 제거
    countVec = CountVectorizer(max_features=10000, stop_words='english')

    # 영화 키워드 벡터라이징
    dataVectors = countVec.fit_transform(xMovie).toarray()

    # 코사인 유사도
    similarity = cosine_similarity(dataVectors)
    
    # 유사도 내림차순 5개 영화의 인덱스
    idx_collection = []
    for i in idx:
        distances = similarity[i]
        listofMovies = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:7]
        idx_collection.extend(listofMovies)
 
    # 인덱스를 pk로 바꾸기
    pk_collection = []
    for idx in idx_collection:
        pk_collection.append(movies.data[idx[0]]['pk'])

    return pk_collection

# 좋아요 누른 영화 리스트
@api_view(['GET'])
def user_like_movie(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = UserLikeMovieListSerializer(user)

    return Response(serializer.data)

# 좋아요 한 영화와 비슷한 영화 보기
@api_view(['GET'])
def similar_like_movie(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = UserLikeMovieListSerializer(user)
    movies = get_list_or_404(Movie)
    movies_serializer = MovieListSerializer(movies, many=True)
    

    # user가 좋아요한 영화 key값 담기
    movie_key = [data['pk'] for data in serializer.data.get('like_movies')]

    # user가 좋아요 한 영화 index 담기
    idx = []
    for key in movie_key:
        for i in range(len(movies_serializer.data)):
            if key == movies_serializer.data[i]['pk']:
                idx.append(i)
                break
    # words 담기
    print(movies_serializer.data)
    xMovie = [data.get('words') for data in movies_serializer.data]
    # 유사 영화 pk 반환
    result = recommend_movies_names(xMovie, idx, movies_serializer)
    # 유사 영화 pk 기반 querySet 생성
    final_movie = [get_object_or_404(Movie, pk=i) for i in result]
    final_serializer = UserChoiceSimilarMovieSerializer(final_movie, many=True)

    return Response(final_serializer.data)

# 싫어요 누른 영화 리스트
@api_view(['GET'])
def user_dislike_movie(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = UserDislikeMovieListSerializer(user)

    return Response(serializer.data)

# 싫어요 한 영화와 비슷한 영화 보기
@api_view(['GET'])
def similar_dislike_movie(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = UserDislikeMovieListSerializer(user)
    movies = get_list_or_404(Movie)
    movies_serializer = MovieListSerializer(movies, many=True)
    
    # user가 싫어여한 영화 key값 담기
    movie_key = [data['pk'] for data in serializer.data.get('dislike_movies')]

    # user가 싫어요 한 영화 index 담기
    idx = []
    for key in movie_key:
        for i in range(len(movies_serializer.data)):
            if key == movies_serializer.data[i]['pk']:
                idx.append(i)
                break
    # words 담기
    xMovie = [data.get('words') for data in movies_serializer.data]

    # 유사 영화 pk 반환
    result = recommend_movies_names(xMovie, idx, movies_serializer)

    # 유사 영화 pk 기반 querySet 생성
    final_movie = [get_object_or_404(Movie, pk=i) for i in result]
    final_serializer = UserChoiceSimilarMovieSerializer(final_movie, many=True)

    return Response(final_serializer.data)

# 좋아요한 영화에서 싫어요한 영화 제외해서 보여주기
@api_view(['GET'])
def user_filtered_movie(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    
    # 좋아요 한 영화
    like_serializer = UserLikeMovieListSerializer(user)
    like_movies = [data['pk'] for data in like_serializer.data.get('like_movies')]

    # 싫어요 한 영화
    dislike_serializer = UserDislikeMovieListSerializer(user)
    dislike_movies = [data['pk'] for data in dislike_serializer.data.get('dislike_movies')]

    # 모든 영화 데이터 가져오기
    movies = get_list_or_404(Movie)
    movies_serializer = MovieListSerializer(movies, many=True)

    # 좋아요 한 영화 index 담기
    like_idx = []
    for key in like_movies:
        for i in range(len(movies_serializer.data)):
            if key == movies_serializer.data[i]['pk']:
                like_idx.append(i)
                break

    # 싫어요 한 영화 index 담기
    dislike_idx = []
    for key in dislike_movies:
        for i in range(len(movies_serializer.data)):
            if key == movies_serializer.data[i]['pk']:
                dislike_idx.append(i)
                break

    # words 담기
    xMovie = [data.get('words') for data in movies_serializer.data]

    # 유사 영화 pk 반환 (싫어하는 영화 유사 영화 제외)
    result = recommend_movies_names_exclude_disliked(xMovie, like_idx, dislike_idx, movies_serializer)

    # 유사 영화 pk 기반 querySet 생성
    final_movie = [get_object_or_404(Movie, pk=i) for i in result]
    final_serializer = UserChoiceSimilarMovieSerializer(final_movie, many=True)

    return Response(final_serializer.data)
