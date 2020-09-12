import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data
import datetime

start = datetime.datetime(2019, 9, 9)
end = datetime.datetime(2020, 9, 9)
ticker = 'aapl'

def get_data(ticker, start_date, end_date):
    df = data.DataReader(ticker, 'yahoo', start_date, end_date)
    return df

def get_close_price_history(ticker, start_datetime, end_datetime):
    df = get_data(ticker, start_datetime, end_datetime)
    closes = list(df['Close'])
    dates_and_closes = [[df.index[i], closes[i]] for i in range(len(df))]
    df_dates_closes = pd.DataFrame(dates_and_closes, columns=['date', 'price'])
    return df_dates_closes

def get_moving_average(ticker, start_datetime, end_datetime, n=50):
    td = datetime.timedelta(days=n)
    start = start_datetime - td
    end = end_datetime

    prices = get_close_price_history(ticker, start, end)

    columns = ['date', 'MA_price']
    moving_averages = []
    for i in range(n, len(prices)):
        price_slice = list(prices.loc[i-n: i]['price'])
        moving_average = sum(price_slice)/n
        moving_averages.append([prices.loc[i]['date'], moving_average])

    ma_df = pd.DataFrame(moving_averages, columns=columns)
    return ma_df


def plot_data(ticker, start, end):
    prices = get_close_price_history(ticker, start, end)
    x = list(prices['date'])
    y = list(prices['price'])

    ma_prices_50 = get_moving_average(ticker, start, end)
    ma_x_50 = list(ma_prices_50['date'])
    ma_y_50 = list(ma_prices_50['MA_price'])

    ma_prices_15 = get_moving_average(ticker, start, end, 15)
    ma_x_15 = list(ma_prices_15['date'])
    ma_y_15 = list(ma_prices_15['MA_price'])

    plt.title(ticker.upper())
    plt.plot(x, y)
    plt.plot(ma_x_50, ma_y_50)
    plt.plot(ma_x_15, ma_y_15)
    plt.show()

