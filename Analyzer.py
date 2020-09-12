from Scraper import ScrapedMorningstarNews
from Scraper import ScrapedFinvizNews
import os

from nltk.sentiment.vader import SentimentIntensityAnalyzer

#magnifying the effects of positive or negative language specific to financial news.
'''for i in new_words:
    new_words[i] *= 3.5'''

analyzer = SentimentIntensityAnalyzer()
#analyzer.lexicon.update(new_words)

sentiment_val_list = []

def get_morningstar_sentiment(ticker, exchange):
    news_content = ScrapedMorningstarNews(ticker, exchange)

    headline_scores = news_content['headline'].apply(analyzer.polarity_scores).tolist()

    avg = 0
    n = len(headline_scores)
    for i in range(n):
        avg += float(headline_scores[i]['compound'])
    avg /= n
    sentiment_val_list.append(avg)
    return avg

def get_finviz_sentiment(ticker):
    news_content = ScrapedFinvizNews(ticker)
    headline_scores = news_content['headline'].apply(analyzer.polarity_scores).tolist()

    avg = 0
    n = len(headline_scores)
    for i in headline_scores:
        avg += float(i['compound'])
    avg /= n
    sentiment_val_list.append(avg)
    return avg


def get_overall_sentiment(ticker):
    #m_star = get_morningstar_sentiment(ticker, exchange)
    finviz = get_finviz_sentiment(ticker)
    avg = 0
    n = 0
    for i in sentiment_val_list:
        if i is None:
            continue
        n += 1
        avg += i
    if n == 0:
        return "No relevant news detected."
    return avg/n

def get_sentiment_from_watchlist(watchlist):
    sentiments = []
    for i in watchlist:
        sentiment = round(get_overall_sentiment(i['ticker']),3)
        sentiments.append(sentiment)

    return sentiments