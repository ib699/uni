import json
from PyMovieDb import IMDB

"""
from https://github.com/itsmehemant7/PyMovieDb
"""


def search(name):
    imdb = IMDB()
    response = imdb.get_by_name(name, tv=True)
    if not json.dumps(response) or response['message'] == 'No Result Found!':
        return None
    else:
        return json.dumps(response)

# print(search("Forrest Gump"))
