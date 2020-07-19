import textblob
from statistics import mean
from textblob import TextBlob
import pandas as pd


## Analytic Helper Functions ##
def __parse_text_to_date_and_text_dict(text):
    sentiment_and_subjectivety = {}
    for date in text.keys():
        temp_list = []
        for piece in text[date]:
            blob = TextBlob(piece)
            temp_list.append((blob.polarity, blob.subjectivity))
        sentiment_and_subjectivety[date] = temp_list
    return sentiment_and_subjectivety


def __quick_parse(date_to_text):
    return {date: [TextBlob(text).sentiment for text in texts] for date, texts in date_to_text.items()}

def __from_sentiment_to_avg(date_to_sentiment):
    return {date: (mean([sentiment.polarity for sentiment in sentiments]), mean([sentiment.subjectivity for sentiment in sentiments])) for date, sentiments in date_to_sentiment.items()}

def __get_dict_as_dataframe(data):
    return pd.DataFrame(data.values(), index=data.keys(), columns=["Mood", "Personal"])

def analyse_list_of_text(text):
    sentiment_and_subjectivety = __quick_parse(text)
    date_to_averages = __from_sentiment_to_avg(sentiment_and_subjectivety)
    data_as_df = __get_dict_as_dataframe(date_to_averages)
    data_as_df.index.name = "Date"
    return data_as_df


if __name__ == "__main__":
    random_list = {
        "1" : ["I hate chairs", "I like lamp", "This was great, ANOTHER"],
        "2" : ["I had a really bad day", "war is a terrible thing"],
        "3" : ["I cut you down to size", "you suck"]
    }
    data = analyse_list_of_text(random_list)
    print(1)
