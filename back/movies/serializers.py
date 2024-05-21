from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

# 영화 목록
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('pk', 'title', 'poster_image')


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
            fields = '__all__'

    genres = GenreSerializer(read_only=True, many=True)
    actors = ActorSerializer(read_only=True, many=True)
    like_movies = UserSerializer(read_only=True, many=True)
    dislike_movies = UserSerializer(read_only=True, many=True)

    class DirectorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Director
            fields = '__all__'

    class Meta:
        model = Movie
        exclude = (
            'popularity',
            'tagline',
            'vote_count',
        )

# 키워드
class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('id', 'name')

# 영화 추찬
class RecommendedSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            field = ('pk', 'title', 'poster_image')

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
            'title',
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
            fields = ('title', 'poster_image', 'pk')

    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = '__all__'

# 검색한 영화와 비슷한 영화
class MovieSearchSerializer(serializers.ModelSerializer):

    similarity = serializers.FloatField(default=0)

    class Meta:
        model = Movie
        fields = ('pk', 'title', 'poster_image', 'similarity')

# 검색한 배우와 비슷한 배우
class ActorSearchSerializer(serializers.ModelSerializer):

    similarity = serializers.FloatField(default=0)

    class Meta:
        model = Actor
        fields = ('pk', 'name', 'profile_image', 'movies', 'similarity',)

# 좋아요한 영화
class UserLikeMovieListSerializer(serializers.ModelSerializer):
    
    class MovieSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ('pk', 'title', 'poster_image')
 
    like_movies = MovieSerializer(many=True)
    
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'like_movies',)

# 싫어요한 영화
class UserDislikeMovieListSerializer(serializers.ModelSerializer):
    
    class MovieSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ('pk', 'title', 'poster_image')
 
    dislike_movies = MovieSerializer(many=True)
    
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'dislike_movies',)

# 추천 영화
class UserChoiceSimilarMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title', 'poster_image', 'pk')

# 감독 디테일
class DirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = '__all__'