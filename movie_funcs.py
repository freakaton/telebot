import json
import http.client
import urllib 

#Take JSON HTTPS response and return dict
def resToDict(res):
    data = res.read().decode('utf-8')
    data = json.loads(data)
    return data

def getMovieById(conn, movieId, token):
    conn.request("GET", "/3/movie/%s?api_key=%s" % (movieId, token))
    res = conn.getresponse()
    data = resToDict(res)
    print('***', data['title'], '***\n\n', data['overview'])

def getMoviesListByQuery(query, token):
    conn = http.client.HTTPSConnection('api.themoviedb.org')
    query = urllib.parse.quote(query)
    conn.request("GET", "/3/search/movie?query=%s&include_adult=true&page=1&api_key=%s" % (query, token))
    res = conn.getresponse()
    data = resToDict(res)
    movies = []
    for movie in data['results']:
        title = movie['title']
        id = movie['id']
        movie = {'title':title, 'id':id}
        movies.append(movie)
    conn.close()
    return movies


