from Scraper import ScrapedMorningstarNews
from Scraper import ScrapedFinvizNews
import os

from nltk.sentiment.vader import SentimentIntensityAnalyzer

'''new_words = {
    'risky': -1.4,
    'high-risk': -1.5,
    'high risk': -1.5,
    'sell': -3.5,
    'should sell': -3.0,
    'down': -1.0,
    'ended down': -1.0,
    'soar': 2.0,
    'soaring': 2.0,
    'take off': 1.5,
    'taking off': 1.5,
    'rise': 0.75,
    'rising': 0.75,
    'steady rise': 0.5,
    'steadily rising': 0.5,
    'climb': 0.5,
    'climbing': 0.5,
    'wrong': -0.5,
    'incorrect': -0.5,
    'debt': -1.0,
    'large debt': -1.0,
    'plummet': -2.0,
    'plunge': -2.0,
    'dive': -1.5,
    'dip': -0.75,
    'drop': -0.75,
    'crash': -2.0,
    'buy': 2.5,
    'hold': -0.75,
    'large potential': 2.5,
    'little potential': -2.5,
    'surge': 2.6,
    'rose': 1.8,
    'win': 2.5,
    'winner': 2.5,
    'loser': -2.5,
    'lose': -2.5,
    'lost': -2.5,
    'gain': 1.8,
    'gains': 1.8,
    'small gain': 1.5,
    'large gain': 2.0,
    'boosts price target': 3.0,
    'higher price target': 3.0,
    'lower price target': -2.5,
    'lowers price target': -2.5,
    'price target hike': 3.0,
    'price target hikes': 3.0,
    'bullish': 2.0,
    'is bullish': 2.0,
    'bearish': -2.0,
    'is bearish': -2.0,
    'rallies': 2.0,
    'rally': 2.0,
    'jump': 1.7,
    'jumps': 1.7,
    'beats': 1.8,
    'beat': 1.8,
    'deal': 1.0,
    'breaking out': 2.0,
    'break out': 2.0,
    'outperforms': 2.5,
    'underperforms': -2.5,
    'beats market': 2.5,
    'lead': 2.0,
    'leads': 2.0,
    'leading': 2.0,
    'tumble': -3.0,
    'tumbles': -3.0,
    'pops': 2.5,
    'popping': 2.5,
    'popped': 2.5,
    'rocket': 3.0,
    'rockets': 3.0,
    'rocketing': 3.0,
    'rocketed': 3.0,
    'skyrocket': 3.0,
    'skyrocketing': 3.0,
    'skyrockets': 3.0,
    'skyrocketed': 3.0
}'''

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