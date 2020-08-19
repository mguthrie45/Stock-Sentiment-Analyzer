from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import os

def ScrapedMorningstarNews(ticker, exchange):
    quote_url = f"https://www.morningstar.com/stocks/{exchange}/{ticker}/quote"
    analysis_url = f"https://www.morningstar.com/stocks/{exchange}/{ticker}/analysis"
    news_url = f"https://www.morningstar.com/stocks/{exchange}/{ticker}/news"
    r1 = requests.get(news_url, headers={'User-Agent': 'Mozilla/5.0'})
    if r1.status_code == 403:
        raise Exception(f"Forbidden HTTP Request Error 403.\n request for: {news_url} \n Change request header.")
    html_content = r1.content

    soup = BeautifulSoup(html_content, 'html5lib')
    coverpage_news = soup.find_all(class_='mdc-news-module stock__news-headline')

    num_articles = len(coverpage_news)
    if num_articles == 0 or num_articles is None:
        return None

    news_contents = [] #[title, link, text]
    list_links = []
    list_titles = []
    dates = []

    for i in np.arange(0, num_articles):
        #finding links
        link = 'https://www.morningstar.com' + coverpage_news[i].find(class_='mdc-link mdc-news-module__headline mds-link mds-link--no-underline')['href']
        list_links.append(link)

        #finding titles
        title = coverpage_news[i].find(class_='mdc-link mdc-news-module__headline mds-link mds-link--no-underline').get_text()
        list_titles.append(title)

        #grabbing article page text
        page = requests.get(link)
        page_content = page.content
        page_soup = BeautifulSoup(page_content, 'html5lib')
        article_body = page_soup.find(class_='mdc-article-body')
        news_paragraphs = article_body.find_all('p', class_='mdc-article-paragraph')

        #grabbing the date
        date_holder = coverpage_news[i].find(class_="mdc-news-module__date")
        date = date_holder['datetime']
        dates.append(date)

        #combining the paragraphs into one element
        article = ''
        p_list = []
        for j in np.arange(0, len(news_paragraphs)):
            text = news_paragraphs[j].get_text()
            p_list.append(str(text))
        article = ' '.join(p_list)
        news_contents.append([ticker, date, title])
        columns = ['ticker', 'date', 'headline']
    return pd.DataFrame(news_contents, columns=columns)