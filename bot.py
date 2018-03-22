import telebot
import os
from flask import Flask, request
from settings import TOKEN, URL, MOVIEDB_TOKEN, IMAGE_BASE_URL
import movie_funcs
from handful_funcs import showListOfMovies, fullDescOfMovie, compareQueryAndMovies

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(commands=['search',])
def search_movies(message):
    searchQuery = message.text.replace('/search ', '')
    movies = movie_funcs.getMoviesListByQuery(searchQuery, MOVIEDB_TOKEN)

    #if only one movie has been found. EXIT
    if len(movies) == 1:
        movie = movies[0]
        image = movie_funcs.getPosterById(movie['id'], MOVIEDB_TOKEN, IMAGE_BASE_URL)
        bot.send_photo(message.chat.id, image)
        bot.send_message(message.chat.id, fullDescOfMovie(movie))
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
            bot.send_message(message.chat.id, fullDescOfMovie(result))
        bot.send_message(message.chat.id, '''
            Has been found more than 1 movie with this title.\n
            Enter number of movie or /exit to exit 
        ''')
        msg = bot.reply_to(message, showListOfMovies(movies))
        
        #Handle choosing from list of movies 
        def choiceFromList(message):
            nonlocal movies
            text = message.text
            #Exiting from choosing. EXIT
            if text == '/exit':
                return True

            #Checking msg for digitable
            elif text.isdigit():
                #Handle if number not in list. EXIT
                if int(text) > len(movies) or int(text) < 1:
                    bot.reply_to(message, 'Your number not in list :(')
                    return True
                #If in list..
                else:
                    movie = movies[int(text)-1]
                    image = movie_funcs.getPosterById(movie['id'], MOVIEDB_TOKEN, IMAGE_BASE_URL)
                    bot.send_photo(message.chat.id, image)
                    bot.send_message(message.chat.id, fullDescOfMovie(movie))
                    return True
            #If not a digit and not /exit. EXIT
            else:
                bot.reply_to(message, 'You input not a digit. WHY?!')
                return True

        bot.register_next_step_handler(msg, choiceFromList)

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