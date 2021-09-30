import sqlite3
from sqlite3 import Error
import yahoofinancials as yf
from datetime import datetime


def get_prices(tickers: list)->list:
    """Returns the most recent stock price"""
    get_prices = []
    for t in tickers:
        tkr = yf.YahooFinancials(t)
        data = tkr.get_stock_price_data()[t]
        get_prices.append([t, data['regularMarketPrice']])
    return get_prices


def add_to_db(db_file, tickers):
    """Adds the scraped tickers to the database and calculates positions"""
    now = datetime.now()
    prices = get_prices(tickers)
    conn = create_connection(db_file)
    db = conn.cursor() 
    # Add the price to the database and determine the holding period return
    for price in prices:
        ticker = price[0]
        value = price[1]
        db.execute('SELECT price FROM aemklg WHERE Ticker = ? ORDER BY'
                   'DateTime DESC LIMIT 1;')


def update_margin_interest_pmts():
    """Insert the compounded cost of having used margin"""
    pass


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
