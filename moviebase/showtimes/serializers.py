from rest_framework import serializers
from datetime import datetime, timedelta

from movielist.models import Movie
from showtimes.models import Cinema, Screening


class CinemaSerializer(serializers.HyperlinkedModelSerializer):
    movies = serializers.SerializerMethodField()

    class Meta:
        model = Cinema
        fields = ('id', 'name', 'city', 'movies')

    def get_movies(self, cinema):
        movies = cinema.movies.filter(screening__date__lt=datetime.now() + timedelta(days=30),
                                      screening__date__gte=datetime.now())
        return [movie.title for movie in movies]


class ScreeningSerializer(serializers.ModelSerializer):
    cinema = serializers.SlugRelatedField(slug_field='id', queryset=Cinema.objects.all())
    cinema_name = serializers.SerializerMethodField()

    class Meta:
        model = Screening
        fields = ('id', 'movie', 'cinema_name', 'cinema', 'date')

    def get_cinema_name(self, obj):
        return obj.cinema.name


class ScreeningSerializerWrite(serializers.ModelSerializer):
    cinema = serializers.SlugRelatedField(slug_field='id', queryset=Cinema.objects.all())

    class Meta:
        model = Screening
        fields = ('id', 'movie', 'cinema', 'date')

