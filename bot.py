import time

import telebot
import flask

import settings
import movie_funcs
from handful_funcs import showListOfMovies, fullDescOfMovie, compareQueryAndMovies

bot = telebot.TeleBot(settings.TOKEN)
server = flask.Flask(__name__)


@server.route("/", methods=['GET', 'HEAD'])
def index():
    return ''


@server.route(settings.WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, 'Hello, ' + message.from_user.first_name + '\n')
    reply = ''' I can look for movies and get info about those.
    Just type /search to start
    '''
    bot.reply_to(message, reply)


def search_movies(message):
    if message.text == '/exit':
        return True
    searchQuery = message.text
    movies = movie_funcs.getMoviesListByQuery(searchQuery, settings.MOVIEDB_TOKEN)

    # if query doesn't have any correlations with existing movies. EXIT
    if len(movies) == 0:
        msg = bot.reply_to(message, 'I don\'t know a single movie with this title. Try again or type /exit to exit')
        bot.register_next_step_handler(msg, search_movies)
        return True

    # if 1 or more movie has been found
    elif len(movies) >= 1:

        # Handle choosing from list of movies
        def choiceFromList(message):
            nonlocal movies
            text = message.text
            # Checking msg for digitable
            if text.isdigit():
                # Handle if number not in list. EXIT
                if int(text) > len(movies) or int(text) < 1:
                    bot.reply_to(message, 'ERROR. Your number not in list :(\n Select right number from list')
                    bot.register_next_step_handler(message, choiceFromList)
                # If in list..
                else:
                    movie = movies[int(text) - 1]
                    image = movie_funcs.getPosterById(movie['id'], settings.MOVIEDB_TOKEN, settings.IMAGE_BASE_URL)
                    bot.send_photo(message.chat.id, image)
                    msg = bot.send_message(message.chat.id, fullDescOfMovie(movie_funcs.getMovieById(movie['id'],
                                                                                                     settings.MOVIEDB_TOKEN)),
                                           parse_mode="HTML")
                    bot.register_next_step_handler(msg, search_movies)
                    return True
            # If not a digit. RETURN TO CHOICE
            else:
                bot.reply_to(message, 'ERROR. Please, input number of the movie')
                bot.register_next_step_handler(message, choiceFromList)

        result = compareQueryAndMovies(searchQuery, movies)
        # if only one movie with same name as query exist
        if result:
            image = movie_funcs.getPosterById(result['id'], settings.MOVIEDB_TOKEN, settings.IMAGE_BASE_URL)
            bot.send_photo(message.chat.id, image)
            msg = bot.send_message(message.chat.id, fullDescOfMovie(movie_funcs.getMovieById(result['id'],
                                                                                             settings.MOVIEDB_TOKEN)),
                                   parse_mode="HTML")
            bot.register_next_step_handler(msg, search_movies)
            return True
        else:
            bot.send_message(message.chat.id, '''
                Has been found more than 1 movie with this title.\n
                Enter number of movie or /exit to exit 
            ''')
            msg = bot.reply_to(message, showListOfMovies(movies))
            bot.register_next_step_handler(msg, choiceFromList)


@bot.message_handler(commands=['search', ])
def search(message):
    msg = bot.reply_to(message, 'send me what you want to search')
    bot.register_next_step_handler(msg, search_movies)


if __name__ == '__main__':
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=settings.WEBHOOK_URL_BASE + settings.WEBHOOK_URL_PATH,
                    certificate=open(settings.WEBHOOK_SSL_CERT, 'r'))
    server.run(host="0.0.0.0",
               port=settings.WEBHOOK_PORT,
               ssl_context=(settings.WEBHOOK_SSL_CERT, settings.WEBHOOK_SSL_PRIV),
               debug=True)
