from django.shortcuts import render_to_response
from movies.models import Movie


def home(request):
    context = {'page': 'home',
               'movies': Movie.objects.all()}
    return render_to_response('home.html', context)

