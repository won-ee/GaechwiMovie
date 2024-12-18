from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.core.paginator import Paginator
from django.db.models import Count, Sum, Case, When, IntegerField
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
    ActorSearchSerializer,
    DirectorSerializer,
    RecommendedSerializer,
)
from .models import Movie, Review, Actor, Director, Keyword, UserKeyword
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

# 키워드 + 1
def add_user_keywords(user, movie):
    # keyword_ids = movie.keywords.all() -> id가 아니라 value 반환
    keyword_ids = movie.keywords.values_list('id', flat=True)
    for keyword_id in keyword_ids:
        keyword = Keyword.objects.get(id=keyword_id)
        user_keyword, created = UserKeyword.objects.get_or_create(user=user, keyword_id=keyword_id)
        user_keyword.count += 1
        user_keyword.save()
    return

# 키워드 - 1
def remove_user_keywords(user, movie):
    keyword_ids = movie.keywords.values_list('id', flat=True)
    for keyword_id in keyword_ids:
        keyword = Keyword.objects.get(id=keyword_id)
        user_keyword, created = UserKeyword.objects.get_or_create(user=user, keyword_id=keyword_id)
        user_keyword.count -= 1
        user_keyword.save()
    return

# 영화 좋아요
@api_view(['POST'])
def like_movie(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    # 좋아요가 눌러져 있을 때
    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        # 키워드-1
        remove_user_keywords(user, movie)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    # 좋아요 안 눌러져 있을 때
    else:
        if movie.dislike_users.filter(pk=user.pk).exists():
            movie.dislike_users.remove(user)
            # 싫어요 취소 되니까 키워드+1
            add_user_keywords(user, movie)
        # 키워드 +1
        movie.like_users.add(user)
        add_user_keywords(user, movie)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
# 영화 싫어요
@api_view(['POST'])
def dislike_movie(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.dislike_users.filter(pk=user.pk).exists():
        movie.dislike_users.remove(user)
        add_user_keywords(user, movie)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    else:
        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user)
            remove_user_keywords(user, movie)
        movie.dislike_users.add(user)
        remove_user_keywords(user, movie)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
# 영화 추천 알고리즘
@api_view(['GET'])
def recommended(request, user_pk, page_pk):
    # count가 0보다 큰 keywords를 추출
    user_keywords = UserKeyword.objects.filter(user_id=user_pk, count__gt=0)
    
    # keywords id 리스트 생성
    keyword_ids = user_keywords.values_list('keyword_id', flat=True)

    # 사용자가 좋아요한 영화 제외하고, 각 키워드의 count 합을 기준으로 큰 순서부터 정렬
    recommended_movies = Movie.objects.filter(
        keywords__in=keyword_ids
    ).exclude(
        like_users__id=user_pk
    ).annotate(
        keyword_match_count=Sum(
            Case(
                *[
                    When(keywords=keyword_id, then=user_keyword.count) 
                    for keyword_id, user_keyword in zip(keyword_ids, user_keywords)
                ],
                default=0,
                output_field=IntegerField()
            )
        )
    ).order_by('-keyword_match_count').distinct()
    
    # 한 페이지당 10개의 데이터 저장
    paginator = Paginator(recommended_movies, 10)
    
    page = request.GET.get('page', page_pk)
    page_movies = paginator.get_page(page)
    serializer = MovieSerializer(page_movies, many=True)
    
    return Response(serializer.data)

    
# 편집거리 알고리즘 - 영화
def search1(lst, keyword):
    fetch_data = []
    for data in lst:
        tmp = {'id': 0, 'title': '', 'poster_image':'', 'similarity':''}
        tmp['id'] = data['id']; tmp['title'] = data['title']; tmp['poster_image'] = data['poster_image']
        tmp['similarity'] = jaro_winkler_similarity(keyword, data['title'])
        fetch_data.append(tmp)
    fetch_data.sort(key=lambda x : -x['similarity'])
    return fetch_data

# 편집거리 알고리즘 - 배우
def search2(lst, keyword):
    fetch_data = []
    for data in lst:
        tmp = {'pk': 0, 'name': '', 'profile_image':'', 'similarity':''}
        tmp['pk'] = data['pk']; tmp['name'] = data['name']; tmp['profile_image'] = data['profile_image']
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

# 좋아요 누른 영화 리스트
@api_view(['GET'])
def user_like_movie(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = UserLikeMovieListSerializer(user)

    return Response(serializer.data)

# 싫어요 누른 영화 리스트
@api_view(['GET'])
def user_dislike_movie(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = UserDislikeMovieListSerializer(user)

    return Response(serializer.data)

# 감독 디테일
@api_view(['GET'])
def director(request, director_pk):
    director = get_object_or_404(Director, pk=director_pk)
    serializer = DirectorSerializer(director)
    return Response(serializer.data)


















# # 추천 알고리즘
# def recommend_movies_names(xMovie, idx, movies):
#     # None값과 빈 문자열을 제거
#     xMovie = [text for text in xMovie if text is not None and text.strip() != '']
#     # 유효한 데이터가 있는 지 확인
#     if not xMovie:
#         return []
#     # 불용어 제거
#     countVec = CountVectorizer(max_features=10000, stop_words='english')

#     # 영화 키워드 벡터라이징
#     dataVectors = countVec.fit_transform(xMovie).toarray()

#     # 코사인 유사도
#     similarity = cosine_similarity(dataVectors)
    
#     # 유사도 내림차순 5개 영화의 인덱스
#     idx_collection = []
#     for i in idx:
#         distances = similarity[i]
#         listofMovies = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:7]
#         idx_collection.extend(listofMovies)
 
#     # 인덱스를 pk로 바꾸기
#     pk_collection = []
#     for idx in idx_collection:
#         pk_collection.append(movies.data[idx[0]]['pk'])

#     return pk_collection

# # 좋아요 한 영화와 비슷한 영화 보기
# @api_view(['GET'])
# def similar_like_movie(request, user_pk):
#     user = get_object_or_404(User, pk=user_pk)
#     serializer = UserLikeMovieListSerializer(user)
#     movies = get_list_or_404(Movie)
#     movies_serializer = MovieListSerializer(movies, many=True)
    

#     # user가 좋아요한 영화 key값 담기
#     movie_key = [data['pk'] for data in serializer.data.get('like_movies')]

#     # user가 좋아요 한 영화 index 담기
#     idx = []
#     for key in movie_key:
#         for i in range(len(movies_serializer.data)):
#             if key == movies_serializer.data[i]['pk']:
#                 idx.append(i)
#                 break
#     # words 담기
#     xMovie = [data.get('words') for data in movies_serializer.data]
#     # 유사 영화 pk 반환
#     result = recommend_movies_names(xMovie, idx, movies_serializer)
#     # 유사 영화 pk 기반 querySet 생성
#     final_movie = [get_object_or_404(Movie, pk=i) for i in result]
#     final_serializer = UserChoiceSimilarMovieSerializer(final_movie, many=True)

#     return Response(final_serializer.data)

# # 싫어요 한 영화와 비슷한 영화 보기
# @api_view(['GET'])
# def similar_dislike_movie(request, user_pk):
#     user = get_object_or_404(User, pk=user_pk)
#     serializer = UserDislikeMovieListSerializer(user)
#     movies = get_list_or_404(Movie)
#     movies_serializer = MovieListSerializer(movies, many=True)
    
#     # user가 싫어여한 영화 key값 담기
#     movie_key = [data['pk'] for data in serializer.data.get('dislike_movies')]

#     # user가 싫어요 한 영화 index 담기
#     idx = []
#     for key in movie_key:
#         for i in range(len(movies_serializer.data)):
#             if key == movies_serializer.data[i]['pk']:
#                 idx.append(i)
#                 break
#     # words 담기
#     xMovie = [data.get('words') for data in movies_serializer.data]

#     # 유사 영화 pk 반환
#     result = recommend_movies_names(xMovie, idx, movies_serializer)

#     # 유사 영화 pk 기반 querySet 생성
#     final_movie = [get_object_or_404(Movie, pk=i) for i in result]
#     final_serializer = UserChoiceSimilarMovieSerializer(final_movie, many=True)

#     return Response(final_serializer.data)

# # 싫어요한 영화는 제외하고 좋아요한 영화와 비슷한 영화들 추천
# def recommend_movies_names_exclude_disliked(xMovie, like_idx, dislike_idx, movies):
#     # None값과 빈 문자열을 제거
#     xMovie = [text for text in xMovie if text is not None and text.strip() != '']
#     # 유효한 데이터가 있는 지 확인
#     if not xMovie:
#         return []
#     # 불용어 제거
#     countVec = CountVectorizer(max_features=10000, stop_words='english')

#     # 영화 키워드 벡터라이징
#     dataVectors = countVec.fit_transform(xMovie).toarray()

#     # 코사인 유사도
#     similarity = cosine_similarity(dataVectors)
    
#     # 유사도 내림차순 5개 영화의 인덱스
#     idx_collection = []
#     for i in like_idx:
#         distances = similarity[i]
#         listofMovies = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:7]
#         idx_collection.extend(listofMovies)
    
#     # 싫어하는 영화와 유사한 영화 제거
#     disliked_movie_set = set()
#     for i in dislike_idx:
#         distances = similarity[i]
#         listofDislikedMovies = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:7]
#         disliked_movie_set.update([idx[0] for idx in listofDislikedMovies])
    
#     # 인덱스를 pk로 바꾸기, 싫어하는 영화 제외
#     pk_collection = []
#     for idx in idx_collection:
#         if idx[0] not in disliked_movie_set:
#             pk_collection.append(movies.data[idx[0]]['pk'])

#     return pk_collection

# # 좋아요한 영화에서 싫어요한 영화 제외해서 보여주기
# @api_view(['GET'])
# def user_filtered_movie(request, user_pk):
#     user = get_object_or_404(User, pk=user_pk)
    
#     # 좋아요 한 영화
#     like_serializer = UserLikeMovieListSerializer(user)
#     like_movies = [data['pk'] for data in like_serializer.data.get('like_movies')]

#     # 싫어요 한 영화
#     dislike_serializer = UserDislikeMovieListSerializer(user)
#     dislike_movies = [data['pk'] for data in dislike_serializer.data.get('dislike_movies')]

#     # 모든 영화 데이터 가져오기
#     movies = get_list_or_404(Movie)
#     movies_serializer = MovieListSerializer(movies, many=True)

#     # 좋아요 한 영화 index 담기
#     like_idx = []
#     for key in like_movies:
#         for i in range(len(movies_serializer.data)):
#             if key == movies_serializer.data[i]['pk']:
#                 like_idx.append(i)
#                 break

#     # 싫어요 한 영화 index 담기
#     dislike_idx = []
#     for key in dislike_movies:
#         for i in range(len(movies_serializer.data)):
#             if key == movies_serializer.data[i]['pk']:
#                 dislike_idx.append(i)
#                 break

#     # words 담기
#     xMovie = [data.get('words') for data in movies_serializer.data]

#     # 유사 영화 pk 반환 (싫어하는 영화 유사 영화 제외)
#     result = recommend_movies_names_exclude_disliked(xMovie, like_idx, dislike_idx, movies_serializer)

#     # 유사 영화 pk 기반 querySet 생성
#     final_movie = [get_object_or_404(Movie, pk=i) for i in result]
#     final_serializer = UserChoiceSimilarMovieSerializer(final_movie, many=True)

#     return Response(final_serializer.data)
