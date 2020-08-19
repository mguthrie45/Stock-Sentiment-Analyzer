from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

def ScrapedFinvizNews(ticker): #only a headline scraper, does not scrape articles
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    r1 = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r1.status_code == 403:
        raise Exception(f"Forbidden HTTP Request Error 403.\n request for: {url} \n Change request header.")
    html_content = r1.content

    soup = BeautifulSoup(html_content, 'html5lib')
    news_headlines = soup.find_all('a', class_="tab-link-news")
    dates = soup.find_all()

    num_articles = len(news_headlines)
    if num_articles == 0 or num_articles is None:
        return None

    list_headlines = []
    news_contents = []
    dates = []

    for i in np.arange(0, num_articles):
        headline = news_headlines[i].get_text()
        date = ""
        dates.append(date)
        list_headlines.append(str(headline))
        news_contents.append([ticker, date, headline])
    columns = ['ticker', 'date', 'headline']
    return pd.DataFrame(news_contents, columns=columns)
