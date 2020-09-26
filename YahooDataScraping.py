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

def get_price(ticker):
    now = datetime.datetime.now()
    day_before = now - datetime.timedelta(days=1)
    data = get_close_price_history(ticker, day_before, now)
    return round(data.iloc[0]['price'], 2)

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

def scale_volume(ticker, start, end):
    history = get_close_price_history(ticker, start, end)
    price_history = list(history['price'])
    date_history = list(history['date'])
    df = get_data(ticker, start, end)
    volumes = list(df['Volume'])

    avg_price_overall = 0
    avg_volume_overall = 0
    for i in range(len(price_history)):
        avg_price_overall += float(price_history[i])
        avg_volume_overall += float(volumes[i])
    avg_price_overall /= len(price_history)
    avg_volume_overall /= len(volumes)

    avg_price_overall /= 3
    shrink_factor = avg_price_overall/avg_volume_overall
    for i in range(len(volumes)):
        volumes[i] *= shrink_factor

    return {'volume': volumes, 'date': date_history, 'shrinkfactor': shrink_factor}


def plot_data(ticker, start, end, ma15True, ma50True, volTrue):
    df = get_data(ticker, start, end)
    prices = get_close_price_history(ticker, start, end)
    x = list(prices['date'])
    y = list(prices['price'])

    plt.title(ticker.upper())
    plt.plot(x, y)

    if ma15True:
        ma_prices_15 = get_moving_average(ticker, start, end, 15)
        ma_x_15 = list(ma_prices_15['date'])
        ma_y_15 = list(ma_prices_15['MA_price'])
        plt.plot(ma_x_15, ma_y_15, label="15-day Moving Average")
    if ma50True:
        ma_prices_50 = get_moving_average(ticker, start, end)
        ma_x_50 = list(ma_prices_50['date'])
        ma_y_50 = list(ma_prices_50['MA_price'])
        plt.plot(ma_x_50, ma_y_50, label="50-day Moving Average")
    if volTrue:
        vol_dict = scale_volume(ticker, start, end)
        vol_values = vol_dict['volume']
        vol_dates = vol_dict['date']
        shrink_factor = vol_dict['shrinkfactor']
        plt.plot(vol_dates, vol_values, label=f"Volume (shrink factor of {shrink_factor: .2e})")


    plt.legend()
    plt.show()

