from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters

from showtimes.models import Screening, Cinema
from showtimes.serializers import ScreeningSerializer, CinemaSerializer, ScreeningSerializerWrite


class ScreeningListView(generics.ListCreateAPIView):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('movie__title', 'cinema__city')


class ScreeningView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializerWrite


class CinemaListView(generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class CinemaView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer
