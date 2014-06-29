from django.shortcuts import render_to_response
from movies.models import Movie, Genre, Collection


def _nav_bar(context):
    collection, _ = Collection.objects.get_or_create(name="Initial Collection")
    context.update({
        'movie_count': collection.movies.count(),
        'genre_count': Genre.objects.all().count()})
    return context


def home(request):
    collection, _ = Collection.objects.get_or_create(name="Initial Collection")
    context = {'page': 'home',
               'movies': collection.movies}
    context = _nav_bar(context)
    return render_to_response('home.html', context)

