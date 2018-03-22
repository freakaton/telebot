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
    searchQuery = str(message.text)
    movies = movie_funcs.getMoviesListByQuery(searchQuery.replace('/search ', ''), MOVIEDB_TOKEN)
    reply = ''
    for movie in movies:
        reply += '//' + movie['title'] + ' - '  + str(movie['id']) + '\n'
    msg = bot.reply_to(message, reply)
    print('replied')
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