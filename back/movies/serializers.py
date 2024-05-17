from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('pk', 'title', 'poster_path')


# 단일 영화 상세 정보
class MovieSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'nickname', 'profile_pic')

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


class ReviewSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'nickname', 'profile_pic')

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
