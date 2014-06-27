from django.shortcuts import render_to_response
from movies.models import Movie, Genre


def _nav_bar(context):
    context.update({
        'movie_count': Movie.objects.all().count(),
        'genre_count': Genre.objects.all().count()})
    return context


def home(request):
    context = {'page': 'home',
               'movies': Movie.objects.all()}
    context = _nav_bar(context)
    return render_to_response('home.html', context)

