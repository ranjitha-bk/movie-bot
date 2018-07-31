from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from watson_developer_cloud import ConversationV1
import json
import requests
from urllib.request import urlopen
context = None


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    print('Received /start command')
    update.message.reply_text('Hi!')


def help(bot, update):
    print('Received /help command')
    update.message.reply_text('Help!')


def message(bot, update):
    print('Received an update')
    global context

    conversation = ConversationV1(username='your_username_here',  # TODO
                                  password='your_password_here',  # TODO
                                  version='Version_date')

    # get response from watson
    response = conversation.message(
        workspace_id='your_workspace_id_here',  # TODO
        input={'text': update.message.text},
        context=context)
    print(json.dumps(response, indent=2))

    context = response['context']
    resp = ''
    for text in response['output']['text']:
        resp += text
    update.message.reply_text(resp)
    context = None

    # build response
    if 'movie' in response['context']:
        movie_name = str(response['context']['movie'])
        url = "http://www.omdbapi.com/?apikey=YOUR_API_KEY=" + movie_name + "&plot=short"
        movies = json.loads(urlopen(url.replace(' ', '%20')).read().decode('utf-8'))
        print('movie')
        update.message.reply_text("Title:"+ movies.get('Title')+"\nYear:"+ movies.get('Year')+"\nGenre:"+ movies.get('Genre')+"\nDirector:"+ movies.get('Director')+"\nActors:"+ movies.get('Actors')+"\nPlot:"+ movies.get('Plot')+"\nIMDB Rating:"+movies.get('imdbRating'))
        context = None
    if 'year' in response['context']:
        year_name = str(response['context']['year'])
        url = "https://api.themoviedb.org/3/discover/movie?primary_release_year=" + year_name + "&sort_by=vote_average.desc&language=en-US&api_key=YOUR_API_KEY"
        print(url)
        movies = json.loads(urlopen(url).read().decode('utf-8'))
        lsa = list()
        for item in movies['results']:
            print(item.get('title'))
            lsa.append(item.get('title'))
        update.message.reply_text(lsa)
        context = None
    if 'actor' in response['context']:
        actor_name = str(response['context']['actor'])
        actor_name.replace(' ', '+')
        print(actor_name)
        url = "http://www.myapifilms.com/imdb/idIMDB?name=" + actor_name + "&token=YOUR_API_KEY&format=json&language=en-us&filmography=1&exactFilter=0&limit=1&bornDied=0&starSign=0&uniqueName=0&actorActress=0&actorTrivia=0&actorPhotos=0&actorVideos=0&salary=0&spouses=0&tradeMark=0&personalQuotes=0&starMeter=0&fullSize=0&alternateNames=0"
        url = url.replace(' ', '+')
        print(url)
        movies = json.loads(urlopen(url.replace(' ', '+')).read().decode('utf-8'))
        lsact = list()
        result = movies['data']['names'][0]
        for result1 in result['filmographies']:
            for result2 in result1['filmography']:
                lsact.append(result2['title'])
                
        update.message.reply_text(lsact)
        print(lsact)
        context = None
    if 'popular' in response['context']:
        print('popular')
        url = "https://api.themoviedb.org/3/discover/movie?order_by=popularity.Modified%20desc&page=1/%20&api_key=YOUR_API_KEY"
        print(url)
        movies = json.loads(urlopen(url).read().decode('utf-8'))
        lsp = list()
        for item in movies['results']:
            print(item.get('title'))
            lsp.append(item.get('title'))
        update.message.reply_text(lsp)
        context = None
    genres = {"action": 28,"adventure":12,"animation":16,"comedy":35,"crime":80,"documentary":99,"drama":18,"family":10751,"fantasy":14,"history":36,"horror":27,"music":10402,"mystery":9648,"romance":10749,"scifi":878,"TV movie":10770,"thriller":53,"war":10752,"western":37}
    if 'genre' in response['context']:
        genre_name = str(response['context']['genre'])
        print(genre_name)
        id = str(genres.get(genre_name))
        url ="https://api.themoviedb.org/3/discover/movie?api_key=YOUR_API_KEY&with_genres=" +id+ "&sort_by=vote_average.desc&vote_count.gte=10"
        movies = json.loads(urlopen(url).read().decode('utf-8'))
        lsg = list()
        print(url)
        for item in movies['results']:
            if str(item['genre_ids'][0])==id:
                lsg.append(item.get('title'))
        update.message.reply_text(lsg)
        context = None


def main():

    # Create the Updater and pass it your bot's token.
    updater = Updater('YOUR_BOTS_TOKEN')  # TODO

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, message))

    # Start the Bot
    updater.start_polling()
    #

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
