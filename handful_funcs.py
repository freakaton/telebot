def showListOfMovies(movies):
    reply = ''
    for movie in movies:
        reply += str(movies.index(movie)+1)+'. '+movie['pprint']+'\n'
    return reply

def fullDescOfMovie(movie):
    reply = '***'+movie['title']+'***\n\n'
    if 'production_countries' in movie:
        countries = []
        for country in movie['production_countries']:
            countries.append(country['name'])
        reply += 'countries: '+', '.join(countries)+'\n'
    if 'genres' in movie:
        genres = []
        for genre in movie['genres']:
            genres.append(genre['name'])
        reply += 'genre: '+', '.join(genres)+'\n'
    if 'runtime' in movie:
        reply += 'length: '+str(movie['runtime'])+' min.\n'
    if 'release_date' in movie:
        reply += 'release date: '+movie['release_date']+'\n'
    if 'overview' in movie:
        reply += 'Overview: \n'+movie['overview']+'\n'
    if 'vote_average' in movie:
        reply += '`'+'vote_average: '+ str(movie['vote_average'])+'/10`\n'
    return reply
        


#search for exactly 1 match of query and movie title
def compareQueryAndMovies(query, movies):
    i = []
    for movie in movies:
        if movie['title'] == query:
            i.append(movie)
    if len(i) == 1:
        return i[0]
    else:
        return False