from django.conf import settings
import requests
import json
import os.path
import time
import re
import urllib


class MovieDB(object):

    def part_of_collection(self, name, year=None):
        results = self.search_for_movie(name, year)
        for result in results.get('results', []):
            if result['release_date'] == '' and result["original_title"].endswith("Collection"):
                return True
        return False

    def get_id(self, name, year=None):
        results = self.search_for_movie(name, year)
        for result in results.get('results', []):
            if result['release_date'] != '' and not result["original_title"].endswith("Collection"):
                return result['id']
        return -1

    def filename_to_title(self, title):
        cleaned = title.replace("_", " ").replace("  ", " ")
        for chunk in ["\n", ",", "*", ".avi", "/", ".mkv", "(", ")", ".mp4"]:
            cleaned = cleaned.replace(chunk, "")
        return cleaned

    def filename_to_year(self, filename):
        m = re.search("\((\d{4})\)", filename)
        if m:
            return m.groups()[0]

    def title_to_filename(self, title):
        cleaned = title
        for chunk in [",", "(", ")", "?", "/", ":", "."]:
            cleaned = cleaned.replace(chunk, "")
        cleaned = cleaned.replace(" ", "_")
        return cleaned

    def do_api_call(self, stored_filename, query_url):

        directory, filename = os.path.split(stored_filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.isfile(stored_filename):
            r = requests.get(query_url)
            data = r.text.encode('utf-8').strip()
            f = open(stored_filename, "w")
            f.write(json.dumps(json.loads(data), sort_keys=True, indent=4, separators=(',', ': ')))
            f.close()
            time.sleep(settings.MOVIEDB_WAIT_TIME)

        else:
            f = open(stored_filename, "r")
            data = f.read()
            data = data.encode('utf-8').strip()
            f.close()

        return json.loads(data)

    def get_configuration(self):
        stored_filename = "./data/images/moviedb__configuration.json"
        query_url = "http://api.themoviedb.org/3/configuration?api_key=%s" % (settings.MOVIEDB_API_KEY)
        results = self.do_api_call(stored_filename, query_url)
        return results

    def get_image_list(self, moviedb_id):
        try:
            stored_filename = "./data/images/moviedb_images_%s.json" % moviedb_id
            query_url = "http://api.themoviedb.org/3/movie/%s/images?api_key=%s" % (moviedb_id, settings.MOVIEDB_API_KEY)
            results = self.do_api_call(stored_filename, query_url)
            return results
        except:
            return

    def search_for_movie(self, title, year=None):
        stored_filename = "./data/moviedb_search_%s.json" % self.title_to_filename(title)

        if year:
            title = title.replace(year, "")
            title = title.strip(" ")
        title = title.encode("ascii", "ignore")

        params = [
            ('api_key', settings.MOVIEDB_API_KEY),
            ('query', title)]

        if year:
            params.append(('year', year))

        query_url = u"http://api.themoviedb.org/3/search/movie?%s" % urllib.urlencode(params)

        results = self.do_api_call(stored_filename, query_url)
        return results

    def get_movie_details(self, name):
        name = self.title_to_filename(name)
        movie_id = self.get_id(name)

    def get_movie_details_by_id(self, movie_id):
        stored_filename = "./data/moviedb_details_%s.json" % movie_id
        query_url = "http://api.themoviedb.org/3/movie/%s?api_key=%s" % (movie_id, settings.MOVIEDB_API_KEY)
        return self.do_api_call(stored_filename, query_url)

    def get_similar_movies(self, movie):
        stored_filename = "./data/moviedb_recommendations_%s.json" % self.title_to_filename(movie.name)
        query_url = "http://api.themoviedb.org/3/movie/%s/similar_movies?api_key=%s" % (movie.moviedb_id, settings.MOVIEDB_API_KEY)
        return self.do_api_call(stored_filename, query_url)