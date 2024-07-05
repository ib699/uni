import json
from PyMovieDb import IMDB

"""
from https://github.com/itsmehemant7/PyMovieDb
"""


def search(name):
    imdb = IMDB()
    response = imdb.get_by_name(name, tv=True)
    if "\"message\": \"No Result Found!\"," in response:
        return None
    else:
        return json.dumps(response)

# print(search("Forrest Gump"))
# print(search("llslwoivn"))
