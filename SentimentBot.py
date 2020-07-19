import textblob
from textblob import TextBlob





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

def analyse_list_of_text(text):
    sentiment_and_subjectivety = __parse_text_to_date_and_text_dict(text)
    return sentiment_and_subjectivety

