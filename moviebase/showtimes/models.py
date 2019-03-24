from django.db import models
from movielist.models import Movie


class Cinema(models.Model):
    name = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    movies = models.ManyToManyField(Movie, through='Screening')

    def __str__(self):
        return self.name


class Screening(models.Model):
    date = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
