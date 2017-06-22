from tasks.base import BaseTask
from movies.models.movies import Movies

class AddMovies(BaseTask):

  SECONDS = 2

  def __str__(self):
    return u"AddMovies"

  def do(self):
    qs = Movies.objects.filter(name=None)
    print "adding movies"
      


