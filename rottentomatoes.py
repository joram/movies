import os
import requests
import time
import json

from django.conf import settings


class RottenTomatoes():

    def __init__(self):
        self.base_url = "http://api.rottentomatoes.com/api/public/v1.0"
        self.api_key = settings.ROTTEN_TOMATO_API_KEY

    def get_recommendation(self, imdb_id):
        url = "%s/movies/%s/similar.json?apikey=%s" % (self.base_url, imdb_id, self.api_key)
        filename = "data/rottentomatoes/test.txt"
        data = self.do_api_call(filename, url)
        print data
        return data

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
            time.sleep(settings.ROTTEN_TOMATO_WAIT_TIME)

        else:
            f = open(stored_filename, "r")
            data = f.read()
            data = data.encode('utf-8').strip()
            f.close()

        return json.loads(data)