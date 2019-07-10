def showListOfMovies(movies):
    reply = ''
    for movie in movies:
        reply += str(movies.index(movie) + 1) + '. ' + movie['pprint'] + '\n'
    return reply


def fullDescOfMovie(movie):
    reply = '***<b>' + movie['title'] + '</b>***\n\n'
    if '<b>production_countries</b>' in movie:
        countries = []
        for country in movie['production_countries']:
            countries.append(country['name'])
        reply += '<b>countries:</b> ' + ', '.join(countries) + '\n'
    if 'genres' in movie:
        genres = []
        for genre in movie['genres']:
            genres.append(genre['name'])
        reply += '<b>genre:</b> ' + ', '.join(genres) + '\n'
    if 'runtime' in movie:
        reply += '<b>length:</b> ' + str(movie['runtime']) + ' min.\n'
    if 'release_date' in movie:
        reply += '<b>release date:</b> ' + movie['release_date'] + '\n'
    if 'overview' in movie:
        reply += '<b>Overview:</b> \n' + movie['overview'] + '\n'
    if 'vote_average' in movie:
        reply += '<b>' + 'vote_average: ' + str(movie['vote_average']) + '/10</b>\n'
    return reply


# search for exactly 1 match of query and movie title
def compareQueryAndMovies(query, movies):
    i = []
    for movie in movies:
        if movie['title'] == query:
            i.append(movie)
    if len(i) == 1:
        return i[0]
    if len(movies) == 1:
        return movies[0]
    else:
        return False
