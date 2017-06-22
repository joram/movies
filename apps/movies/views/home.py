from apps.movies.models import Library
from _helpers import _paginated_movies


def home(request):
    return _paginated_movies(request, movies=Library.objects.default.movies)
