def showListOfMovies(movies):
    reply = ''
    for movie in movies:
        reply += str(movies.index(movie)+1)+'. '+movie['pprint']+'\n'
    return reply

def fullDescOfMovie(movie):
    return '****'+movie['pprint']+'****'
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