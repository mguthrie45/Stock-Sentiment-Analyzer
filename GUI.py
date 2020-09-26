
#TODO: make analysis checkbuttons work
#TODO: Don't make program find sentiment every time it opens up but maintain the every hour rule.
#TODO: get sentiment and stock price vs time graphs
#TODO: Possibly add memory system for daily sentiment prices of each watchlist stock.
#TODO: Make watchlist analysis: "overall watchlist sentiment", cumulative watchlist graphing abilities
#TODO: for watchlist analysis: keep track of when ticker was added and find loss-gain. Have it graphed too since it was on watchlist.





import Analyzer
import tkinter as tk
import datetime
import time
import threading
import sys
from YahooDataScraping import plot_data, get_price

import mail_notifications


#     Dealing with viewing the watchlist
#
#
#
def open_watchlist_window():
    root2 = tk.Tk()
    root2.geometry("500x500")
    root2.title("My Watchlist")

    m = len(watchlist)
    n = 3

    main_frame = tk.Frame(root2, padx=20, pady=20)
    main_frame.pack()

    tk.Label(main_frame, text="Ticker").grid(row=0, column=1, padx=10, pady=2)
    tk.Label(main_frame, text="Shares").grid(row=0, column=2, padx=10, pady=2)
    tk.Label(main_frame, text="Price").grid(row=0, column=3, padx=10, pady=2)
    for i in range(m):
        m_label = tk.Label(main_frame, text=str(i + 1))
        ticker = watchlist[i]['ticker']
        ticker_label = tk.Label(main_frame, text=ticker)
        shares_label = tk.Label(main_frame, text=watchlist[i]['shares'])
        price_label = tk.Label(main_frame, text=f'${get_price(ticker)}')
        m_label.grid(row=i+1, column=0, padx=10, pady=2)
        ticker_label.grid(row=i+1, column=1, padx=10, pady=2)
        shares_label.grid(row=i+1, column=2, padx=10, pady=2)
        price_label.grid(row=i+1, column=3, padx=10, pady=2)

        end = datetime.datetime.now()
        td = datetime.timedelta(days = 180)
        start = end - td

        button_press = lambda ticker=ticker: open_stock_analysis_window(ticker)#plot_data(ticker, start, end)
        analysis_button = tk.Button(main_frame, text='analysis', command=button_press)
        analysis_button.grid(row=i+1, column=4, padx=10, pady=2)
        print(ticker)

    root2.mainloop()


def get_watchlist():
    watchlist_file = open('watchlist.txt', 'r')
    ticker_lines = watchlist_file.read().split('\n')
    for i in range(len(ticker_lines)):
        ticker_lines[i] = ticker_lines[i].split(' ')
    watchlist_file.close()
    watchlist = []
    for i in ticker_lines[:len(ticker_lines)-1]:
        stock_dict = {'ticker': i[0], 'shares': int(i[1])}
        watchlist.append(stock_dict)
    print(watchlist)
    return watchlist


def get_watchlist_len():
    return len(watchlist)




#     Dealing with the analysis window of a stock
#
#
#
def open_stock_analysis_window(ticker):
    root2 = tk.Tk()
    root2.title(ticker)

    main_frame = tk.LabelFrame(root2, text=ticker.upper(), font=header_font, padx=20, pady=20)
    main_frame.pack()

    time_frame = tk.Frame(main_frame, padx=10, pady=10)
    time_frame.grid(row=0, column=0)

    years_var = tk.StringVar(root2)
    years_label = tk.Label(time_frame, text="Years")
    years_input = tk.Entry(time_frame, textvariable=years_var, width=5)
    years_label.grid(row=0, column=0, padx=10, pady=10)
    years_input.grid(row=0, column=1, padx=10, pady=10)
    months_var = tk.StringVar(root2)
    months_label = tk.Label(time_frame, text="Months")
    months_input = tk.Entry(time_frame, textvariable=months_var, width=5)
    months_label.grid(row=1, column=0, padx=10, pady=10)
    months_input.grid(row=1, column=1, padx=10, pady=10)

    variable_frame = tk.Frame(main_frame, padx=10, pady=10)
    variable_frame.grid(row=0, column=1)

    check_button_dict = {'ma15': 0, 'ma50': 0, 'sentiment': 0, 'volume': 0}

    def change_check_values(variable):
        if check_button_dict[variable] == 0:
            check_button_dict[variable] = 1
        else:
            check_button_dict[variable] = 0

    ma15Check = tk.Checkbutton(variable_frame, text="15 Day MA", command=lambda: change_check_values('ma15'))
    ma15Check.grid(row=0, column=0)
    ma50Check = tk.Checkbutton(variable_frame, text="50 Day MA", command=lambda: change_check_values('ma50'))
    ma50Check.grid(row=1, column=0)
    volumeCheck = tk.Checkbutton(variable_frame, text="volume", command=lambda: change_check_values('volume'))
    volumeCheck.grid(row=2, column=0)
    sentiment = tk.Checkbutton(variable_frame, text="Sentiment History", command=lambda: change_check_values('sentiment'))
    sentiment.grid(row=3, column=0)

    execution_frame = tk.Frame(main_frame, padx=10, pady=10)
    execution_frame.grid(row=0, column=2)

    def plot_according_to_variables():
        years = years_var.get()
        months = months_var.get()
        if years == "":
            years = 0
        else:
            years = int(years)
        if months == "":
            months = 0
        else:
            months = int(months)
        days = years*365+months*30

        end = datetime.datetime.now()
        td = datetime.timedelta(days=days)
        start = end - td

        ma15 = check_button_dict['ma15']
        ma50 = check_button_dict['ma50']
        volume = check_button_dict['volume']
        sentiment = check_button_dict['sentiment']
        plot_data(ticker, start, end, ma15, ma50, volume)

    plot_button = tk.Button(execution_frame, text='plot', command=plot_according_to_variables)
    plot_button.pack()

    root2.mainloop()




#     Dealing with creating new tickers in watchlist
#
#
#

def open_new_ticker_window():
    root2 = tk.Tk()
    root2.geometry("150x150")
    root2.title("Add Another Ticker")

    ticker = tk.StringVar(root2)
    new_ticker_label = tk.Label(root2, text="Ticker")
    new_ticker_entry = tk.Entry(root2, textvariable=ticker)
    shares = tk.StringVar(root2)
    shares_label = tk.Label(root2, text="Shares")
    shares_entry = tk.Entry(root2, textvariable=shares)
    add_button = tk.Button(root2, text="Add", command=lambda: add_ticker(ticker.get(), shares.get()), pady=5)
    new_ticker_label.pack()
    new_ticker_entry.pack()
    shares_label.pack()
    shares_entry.pack()
    add_button.pack(pady=10)

    root2.mainloop()


def add_ticker(ticker, shares):
    if ticker in watchlist:
        tk.messagebox.showerror('Add Error', 'Ticker ticker you entered is already in your watchlist.')
        return None
    watchlist_file = open('watchlist.txt', 'a')
    watchlist_file.write(f'{ticker} {shares}\n')
    watchlist.append(ticker)
    watchlist_file.close()


def remove_ticker(ticker):
    if ticker not in watchlist:
        tk.messagebox.showerror('Removal Error', 'The ticker you entered could not be found in your watchlist.')
        return None
    watchlist.remove(ticker)



#     Dealing with updating sentiment and loading previous sentiment
#
#
#
def get_sentiment_list():
    file = open('latest\\latest_sentiment.txt', 'r')
    sentiments = file.read().split('\n')
    file.close()
    '''for i in range(len(sentiments)):
        sentiments[i] = float(sentiments[i])'''
    return sentiments[:len(sentiments ) -1]


def update_sentiments_memory(sentiments):
    file = open('latest\\latest_sentiment.txt', 'w')
    string = ''
    for i in sentiments:
        string += str(i ) +'\n'
    file.write(string)
    file.close()


def update_sentiments():
    global ticker_sentiments
    prev_sentiments = ticker_sentiments
    ticker_sentiments = Analyzer.get_sentiment_from_watchlist(watchlist)
    update_sentiments_memory(ticker_sentiments)
    print(ticker_sentiments)






#     Initializing variables and the master root
#
#
#
watchlist = get_watchlist()
ticker_sentiments = get_sentiment_list()

root = tk.Tk()
root.title("Stock Sentiment Analyzer")
root.geometry("700x500")

header_font = tk.font.Font(family="Helvetica", size=15)




#     Dealing with all the GUI on the main page
#
#
#
watchlist_tool_frame = tk.LabelFrame(root, text='Watchlist Tools', font=header_font, padx=20, pady=20)
watchlist_tool_frame.grid(row=0, column=0, pady=10, padx=10)

get_stock_sentiment_frame = tk.LabelFrame(root, text='Sentiment Lookup', font=header_font, padx=20, pady=20)
get_stock_sentiment_frame.grid(row=0, column=1, pady=10, padx=10)

ticker_var = tk.StringVar()
enterTicker = tk.Label(get_stock_sentiment_frame, text="ticker")
enterTicker.grid(row=0, column=0, pady=2)
tickerButton = tk.Entry(get_stock_sentiment_frame, textvariable=ticker_var, width=10)
tickerButton.grid(row=0, column=1, pady=2, padx=2)

open_watchlist_button = tk.Button(watchlist_tool_frame, text="My Watchlist", command=open_watchlist_window)
open_watchlist_button.pack(pady=10)

ticker_input_var = tk.StringVar()
new_ticker = tk.Button(watchlist_tool_frame, text="add stock", command=open_new_ticker_window)
new_ticker.pack(pady=10)

watchlist_anyl_frame = tk.LabelFrame(root, text='Watchlist Performance', font=header_font, padx=20, pady=20)
watchlist_anyl_frame.grid(row=2, column=0, pady=10, padx=10)
watchlist_sent_var = tk.StringVar()
overall_watchlist_sentiment = tk.Label(watchlist_anyl_frame, textvariable=watchlist_sent_var)
overall_watchlist_sentiment.pack()



notification_frame = tk.LabelFrame(root, text='Recent Sentiment Activity', font=header_font, padx=20, pady=20)
notification_frame.grid(row=2, column=1, pady=10, padx=10)
notification_string_tk = tk.StringVar()
notification_label = tk.Label(notification_frame, textvariable=notification_string_tk)
notification_label.pack()

def write_notifications(notification_dictionary):
    notification_string = ''
    if len(notification_dictionary['notifications']) != 0:
        for i in notification_dictionary['notifications']:
            notification_string += f'{i} \n'
        notification_string_tk.set(notification_string)


def get_sentiment():
    result = Analyzer.get_overall_sentiment(ticker_var.get())

    sentiment_conversion_list = ["Very Poor", "Poor", "Neutral", "Good", "Very Good"]
    n = len(sentiment_conversion_list)
    sentiment.set(f'{round(result, 2)}  {sentiment_conversion_list[int((result / 2 +0.5 )//.2)]}')  # converts range from -1 to 1 to 0 to 1.


sentiment = tk.StringVar()
submit = tk.Button(get_stock_sentiment_frame, text="Scrape Web Data", padx=4, command=get_sentiment)
submit.grid(row=2, column=0, pady=8, padx=2)

sentimentLabel = tk.Label(get_stock_sentiment_frame, textvariable=sentiment)
sentimentLabel.grid(row=2, column=1, pady=8, padx=2)


# Dealing with the threaded process of checking significant changes in sentiment.
#
#
#
def check_sentiment(most_recent_sentiments):
    sentiment_change_dict = get_sentiment_changes(most_recent_sentiments)
    new_sentiments = sentiment_change_dict['sentiments']

    total_shares = [watchlist[i]['shares'] for i in range(len(new_sentiments))]
    weighted_sentiments = [total_shares[i]*new_sentiments[i] for i in range(len(new_sentiments))]
    print(weighted_sentiments)
    sentiment_conversion_list = ["Very Poor", "Poor", "Neutral", "Good", "Very Good"]
    n = len(sentiment_conversion_list)
    cumulative_watchlist_sentiment = round(sum(weighted_sentiments) / sum(total_shares), 2)
    print(cumulative_watchlist_sentiment)
    watchlist_sent_var.set(f'Cumulative Watchlist Sentiment: {cumulative_watchlist_sentiment}  {sentiment_conversion_list[int((cumulative_watchlist_sentiment / 2 + 0.5) // .2)]}')

    notifications_list = sentiment_change_dict['notifications']
    update_sentiment_file(new_sentiments)
    write_notifications(sentiment_change_dict)

    '''mail_notifications.send_mail_SMTP(notification,
                                      "*",
                                      "*",
                                      "*")'''

    t = threading.Timer(3600, lambda: check_sentiment(new_sentiments))#.start()


def get_sentiment_changes(recent_sentiments_list):
    notification_string = ''
    ticker_sentiments = []
    notifications = []
    for i in range(len(watchlist)):
        ticker = watchlist[i]['ticker']
        sentiment = float(Analyzer.get_overall_sentiment(ticker))
        sentiment = round(sentiment, 2)
        ticker_sentiments.append(sentiment)

        sig_change = 0.05
        recent_sentiment = recent_sentiments_list[i]
        if recent_sentiment == 0:
            if sentiment > 0:
                sentiment_change = 'infinite'
            elif sentiment == 0:
                sentiment_change = 0
            else:
                sentiment_change = '-infinite'
        else:
            sentiment_change = (sentiment-recent_sentiment)/recent_sentiment
        if type(sentiment_change) is float and abs(sentiment_change) != 0:
            if abs(sentiment_change) >= sig_change:
                notification = f'Sentiment for {ticker} has changed {round(100*sentiment_change)}%'
                notifications.append(notification)
                notification_string += notification
                print(notification)
        elif type(sentiment_change) is str:
            notification = f'Sentiment for {ticker} has changed {sentiment_change}%'
            notifications.append(notification)
            notification_string += notification
            print(notification)

    if notification_string == '':
        notification_string = "Your watchlist's stocks haven't changed in sentiment recently..."

    print({'sentiments': ticker_sentiments, 'notifications': notifications})
    return {'sentiments': ticker_sentiments, 'notifications': notifications}


def update_sentiment_file(sentiments_list):
    sentiment_file = open('latest_sentiment.txt', 'w')
    write_str = ''
    for i in sentiments_list:
        write_str += f'{i}\n'
    sentiment_file.write(write_str)
    sentiment_file.close()


def parse_sentiment_file():
    sentiment_file = open('latest_sentiment.txt', 'r')
    sentiments = sentiment_file.read().split('\n')
    sentiments = sentiments[:len(sentiments)-1]
    sentiments_floats = []
    for i in range(len(sentiments)):
        sentiments_floats.append(round(float(sentiments[i]), 2))
    sentiment_file.close()
    if len(sentiments_floats) == 0:
        sentiments_floats = [0.0]*len(watchlist)
    return sentiments_floats


def kill_all_processes():

    root.destroy()
    sys.exit(0)


def sentiment_check_on_startup():
    print('Scraping web data and articles...')
    print('Finding significant sentiment changes...')
    initial_sentiments = parse_sentiment_file()
    check_sentiment(initial_sentiments)


sentiment_check_on_startup()
root.protocol("WM_DELETE_WINDOW", kill_all_processes)
root.mainloop()
