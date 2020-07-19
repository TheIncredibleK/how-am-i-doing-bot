import textblob
from statistics import mean
from textblob import TextBlob
import pandas as pd
from os import environ
import os
import tweepy
import shutil

## API Section ##
API_KEY = environ["API_KEY"]
API_SHH_KEY = environ["API_SHH_KEY"]
ACCESS = environ["ACCESS"]
ACCESS_SECRET = environ["ACCESS_SECRET"]

consumer_key = API_KEY
consumer_secret = API_SHH_KEY
access_token = ACCESS
access_token_secret = ACCESS_SECRET
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
API = tweepy.API(auth)
MY_NAME = "how_am_i_doing"
## Twitter Listener ###
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        process_tweet(status)


## Twitter Helper Functions ##

def __get_tweets_as_date_to_text_dict(tweets):
    tweet_to_dict = {}
    for tweet in tweets:
        date = tweet.created_at.strftime("%b %d %Y")
        if tweet_to_dict.keys().__contains__(date):
            tweet_to_dict[date].append(tweet.text)
        else:
            tweet_to_dict[date] = [tweet.text]
    return tweet_to_dict

def __get_list_of_users_tweets(user):
    returned_tweets = API.user_timeline(screen_name=user, count=100)
    return __get_tweets_as_date_to_text_dict(returned_tweets)

def __tweet_user_results(tweet_id, filepath, username):
    print("Sending out media tweet")
    message = "@{} Here's your results! Remember that I'm not an expert, I'm a shitty piece of code written by an idiot.".format(username)
    API.update_with_media(filename=filepath, status=message, in_reply_to_status_id=tweet_id)



## Analytic Helper Functions ##
def __parse_text_to_date_and_text_dict(text):
    sentiment_and_subjectivety = {}
    for date in text.keys():
        temp_list = []
        for piece in text[date]:
            blob = TextBlob(piece)
            temp_list.append((blob.polarity, blob.subjectivity))
        sentiment_and_subjectivety[date] = temp_list

    print("Got sentiment/subjectivity as dict")
    return sentiment_and_subjectivety


def __quick_parse(date_to_text):
    return {date: [TextBlob(text).sentiment for text in texts] for date, texts in date_to_text.items()}

def __from_sentiment_to_avg(date_to_sentiment):
    return {date: (mean([sentiment.polarity for sentiment in sentiments]), mean([sentiment.subjectivity for sentiment in sentiments])) for date, sentiments in date_to_sentiment.items()}

def __get_dict_as_dataframe(data):
    return pd.DataFrame(data.values(), index=data.keys(), columns=["Mood", "Personal"])

def __process_users_tweets(username):
    ## GET users tweets ###
    tweets = __get_list_of_users_tweets(username)
    return analyse_list_of_text(tweets)

def __save_figure_to_named_directory(data, dir):
    image_directory = os.path.join(os.getcwd(), "images")
    full_new_directory = os.path.join(image_directory, dir)
    figure = data.plot().figure
    figure.set_size_inches(10,4)
    filepath = os.path.join(full_new_directory, "{}.png".format(dir))
    if(os.path.isdir(full_new_directory)):
        shutil.rmtree(full_new_directory)
    os.makedirs(full_new_directory, exist_ok=True)
    figure.savefig(filepath)
    return filepath

def __clean_up(filepath):
    if os.path.isfile(filepath):
       os.remove(filepath)
    path = os.path.dirname(filepath)
    if(os.path.isdir(path)):
        os.rmdir(path)

def process_tweet(tweet):
    username = tweet.author.screen_name
    if(username != MY_NAME):
        print("Processing tweet for {}".format(username))
        user_data = __process_users_tweets(username)
        filepath = __save_figure_to_named_directory(user_data, username)
        __tweet_user_results(tweet.id, filepath, username)
        __clean_up(filepath)
        print("Finished tweeting to {}".format(username))
    else:
        print("Not doing it for myself dingus")


## Main Event Loop ###
def analyse_list_of_text(text):
    sentiment_and_subjectivety = __quick_parse(text)
    print("Got sentiment/subjectivity as dict")
    date_to_averages = __from_sentiment_to_avg(sentiment_and_subjectivety)
    print("Got averages")
    data_as_df = __get_dict_as_dataframe(date_to_averages)
    print("Got data")
    data_as_df.index.name = "Date"
    return data_as_df

def keep_bot_going():
    myStream = tweepy.Stream(auth=API.auth, listener=StreamListener())
    print("ONLINE: ")
    myStream.filter(track=['@{} '.format(MY_NAME)])
    while True:
        a = 1
    return

if __name__ == "__main__":
    keep_bot_going()
