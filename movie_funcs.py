import json
import http.client
from urllib.parse import quote


# Take JSON HTTPS response and return dict
def resToDict(res):
    data = res.read().decode('utf-8')
    data = json.loads(data)
    return data


def getMovieById(movieId, token):
    conn = http.client.HTTPSConnection('api.themoviedb.org')
    conn.request("GET", "/3/movie/%s?api_key=%s" % (movieId, token))
    res = conn.getresponse()
    data = resToDict(res)
    data['pprint'] = pprintOfMovie(data)
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
        minMovie = {'title': title,
                    'id': id,
                    'pprint': pprintOfMovie(movie)
                    }
        movies.append(minMovie)
    conn.close()
    return movies


def getPosterById(id, token, baseImageUrl):
    from urllib.request import urlopen
    try:
        movie = getMovieById(id, token)
        imageUrl = baseImageUrl + movie['poster_path']
        return urlopen(imageUrl)
    except Exception:
        return urlopen('https://pp.userapi.com/c638523/v638523274/22a65/-dmvOVVXoA0.jpg')


# Take movie dict and return prettified str
def pprintOfMovie(movie):
    reply = ''
    reply += movie['title']
    reply += '[' + movie['original_language'].upper() + ']'
    reply += ' (' + movie['release_date'][0:4] + ') '
    return reply
