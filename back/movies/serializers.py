from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

# 영화 목록
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('pk', 'title', 'poster_path', 'vote_average', 'vote_count')


# 단일 영화 상세 정보
class MovieSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'nickname', 'profile_pic',)

    user = UserSerializer(read_only=True)

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('name',)

    class ActorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = ('pk', 'name', 'profile_path')

    genres = GenreSerializer(read_only=True, many=True)
    actors = ActorSerializer(read_only=True, many=True)
    like_movies = UserSerializer(read_only=True, many=True)
    dislike_movies = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        exclude = (
            'popularity',
            'tagline',
            'vote_count',
            'words',
        )

# 리뷰
class ReviewSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username', 'profile_pic')

    user = UserSerializer(read_only=True)

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('pk',)

    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            'pk',
            'user',
            'movie',
            'content',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('movie',)

# 배우
class ActorSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('title', 'poster_path', 'pk')

    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ('name', 'profile_path', 'movies')

# 검색한 영화와 비슷한 영화
class MovieSearchSerializer(serializers.ModelSerializer):

    similarity = serializers.FloatField(default=0)

    class Meta:
        model = Movie
        fields = ('pk', 'words', 'title', 'poster_path', 'similarity',)

# 검색한 배우와 비슷한 배우
class ActorSearchSerializer(serializers.ModelSerializer):

    similarity = serializers.FloatField(default=0)

    class Meta:
        model = Actor
        fields = ('pk', 'name', 'profile_path', 'movies', 'similarity',)

# 좋아요한 영화
class UserLikeMovieListSerializer(serializers.ModelSerializer):
    
    class MovieSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ('pk', 'title', 'poster_path')
 
    like_movies = MovieSerializer(many=True)
    
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'like_movies',)

# 싫어요한 영화
class UserDislikeMovieListSerializer(serializers.ModelSerializer):
    
    class MovieSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ('pk', 'title', 'poster_path')
 
    dislike_movies = MovieSerializer(many=True)
    
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'dislike_movies',)

# 추천 영화
class UserChoiceSimilarMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title', 'poster_path', 'pk')