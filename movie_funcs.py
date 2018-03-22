import json
import http.client
from urllib.parse import quote

#Take JSON HTTPS response and return dict
def resToDict(res):
    data = res.read().decode('utf-8')
    data = json.loads(data)
    return data


def getMovieById(movieId, token):
    conn = http.client.HTTPSConnection('api.themoviedb.org')
    conn.request("GET", "/3/movie/%s?api_key=%s" % (movieId, token))
    res = conn.getresponse()
    data = resToDict(res)
    conn.close()
    return data


def getMoviesListByQuery(query, token):
    conn = http.client.HTTPSConnection('api.themoviedb.org')
    query = quote(query)
    conn.request("GET", "/3/search/movie?query=%s&include_adult=true&page=1&api_key=%s" % (query, token))
    res = conn.getresponse()
    data = resToDict(res)
    movies = []
    for movie in data['results']:
        title = movie['title']
        id = str(movie['id'])
        date = movie['release_date']
        lang = movie['original_language']
        movie = {'title':title,
                 'id':id,
                 'year':date[0:4],
                 'language':lang.upper()
                 }
        movies.append(movie)
    conn.close()
    return movies

def getPosterById(id, token, baseImageUrl):
    from urllib.request import urlopen

    movie = getMovieById(id, token)
    imageUrl = baseImageUrl + quote(movie['poster_path'])
    return urlopen(imageUrl)


