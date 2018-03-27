import telebot
import os
from flask import Flask, request
from settings import TOKEN, URL, MOVIEDB_TOKEN, IMAGE_BASE_URL
import movie_funcs
from movie_funcs import getMovieById
from handful_funcs import showListOfMovies, fullDescOfMovie, compareQueryAndMovies
from telebot import types
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, 'Hello, ' + message.from_user.first_name+'\n')
    reply = ''' I can look for movies and get info about those.
    Just type /search to start
    '''
    bot.reply_to(message, reply)

def search_movies(message):
    searchQuery = message.text
    movies = movie_funcs.getMoviesListByQuery(searchQuery, MOVIEDB_TOKEN)

    #if only one movie has been found. EXIT
    if len(movies) == 1:
        movie = movies[0]
        image = movie_funcs.getPosterById(movie['id'], MOVIEDB_TOKEN, IMAGE_BASE_URL)
        bot.send_photo(message.chat.id, image)
        bot.send_message(message.chat.id, fullDescOfMovie(getMovieById(movie['id'], MOVIEDB_TOKEN)))
        return True

    #if query doesn't have any correlations with existing movies. EXIT
    elif len(movies) == 0:
        bot.reply_to(message, 'I don\'t know a single movie with this title')
        return True

    #if more than 1 movie has been found
    elif len(movies) > 1:
        result = compareQueryAndMovies(searchQuery, movies)
        if result:
            image = movie_funcs.getPosterById(result['id'], MOVIEDB_TOKEN, IMAGE_BASE_URL)
            bot.send_photo(message.chat.id, image)
            bot.send_message(message.chat.id, fullDescOfMovie(getMovieById(result['id'], MOVIEDB_TOKEN)))
        bot.send_message(message.chat.id, '''
            Has been found more than 1 movie with this title.\n
            Enter number of movie or /exit to exit 
        ''')
        msg = bot.reply_to(message, showListOfMovies(movies))
        
        #Handle choosing from list of movies 
        def choiceFromList(message):
            nonlocal movies
            text = message.text
            if message.text == '/exit':
                return True
            #Checking msg for digitable
            elif text.isdigit():
                #Handle if number not in list. EXIT
                if int(text) > len(movies) or int(text) < 1:
                    bot.reply_to(message, 'ERROR. Your number not in list :(\n Select right number from list')
                    bot.register_next_step_handler(message, choiceFromList)
                #If in list..
                else:
                    movie = movies[int(text)-1]
                    image = movie_funcs.getPosterById(movie['id'], MOVIEDB_TOKEN, IMAGE_BASE_URL)
                    bot.send_photo(message.chat.id, image)
                    bot.send_message(message.chat.id, fullDescOfMovie(getMovieById(movie['id'], MOVIEDB_TOKEN)), parse_mode="HTML")
                    return True
            #If not a digit and not /exit. EXIT
            else:
                bot.reply_to(message, 'ERROR. Please, input number of the movie')
                bot.register_next_step_handler(message, choiceFromList)

        bot.register_next_step_handler(msg, choiceFromList)

@bot.message_handler(commands=['search',])
def search(message):
    msg = bot.reply_to(message, 'Ok, send me search query, please')
    bot.register_next_step_handler(msg, search_movies)


@bot.message_handler(commands = ['poster',])
def posterPost(message):
    msg = message.text.replace('/poster ', '')
    if not msg.isdigit():
        bot.reply_to(message, 'Please, enter id of the movie!')
    image = movie_funcs.getPosterById(msg, MOVIEDB_TOKEN, IMAGE_BASE_URL)
    print('image has been received!')
    bot.send_photo(message.chat.id, image)
    
    


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url = URL + TOKEN)
    return "!", 200

server.run(host="0.0.0.0", port=int(os.environ.get('PORT', '8443')))
