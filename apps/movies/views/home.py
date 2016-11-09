from apps.movies.models import Library
from _helpers import _paginated_movies


def home(request):
    library = Library.objects.default
    movies_qs = library.movies
    return _paginated_movies(request, movies=movies_qs)
