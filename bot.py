import telebot
import os
from flask import Flask, request
from settings import TOKEN, URL, MOVIEDB_TOKEN, IMAGE_BASE_URL
import movie_funcs

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(commands=['search',])
def search_movies(message):
    searchQuery = message.text.replace('/search ', '')
    movies = movie_funcs.getMoviesListByQuery(searchQuery, MOVIEDB_TOKEN)
    if len(movies) == 1:
        movieId = movies[0]['id']
        movie = movie_funcs.getMovieById(movieId, MOVIEDB_TOKEN)
        reply = str(movie)
        bot.reply_to(message, reply)
        return True
    elif len(movies) == 0:
        bot.reply_to(message, 'I don\'t know a single movie with this title')
        return True
    elif len(movies) > 1:
        i = []
        for movie in movies:
            if movie['title'] == searchQuery:
                i.append(movie)
        if len(i) == 1:
            movieId = movies[0]['id']
            movie = movie_funcs.getMovieById(movieId, MOVIEDB_TOKEN)
            image = movie_funcs.getPosterById(movieId, MOVIEDB_TOKEN, IMAGE_BASE_URL)
            bot.send_photo(message.chat.id, image)
            reply = str(movie)
            bot.send_message(message.chat.id, reply)
            return True
        elif len(i) > 1:
            bot.send_message(message.chat.id, 'I have found more than 1 movie with this title')
            return True
        else:
            reply = str(movies)
            bot.reply_to(message, reply)
            return True
    else:
        bot.reply_to(message, 'There is some error. Sry')
        return False

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