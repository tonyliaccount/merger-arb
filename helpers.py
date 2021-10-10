# import sqlite3
# from sqlite3 import Error
# from sqlite3.dbapi2 import enable_callback_tracebacks
# import yahoofinancials as yf
# from datetime import datetime


def calculate_merger(days: int, stocks: list, exchange_rate: float,
                     margin_interest: float, commission: float,
                     position_size: float, initial_margin: float) -> float:
    """Given an expected merger transaction, calculate the return of a long
    short position based on the apparent premium or discount.
    Args:
        days (int): number of days to hold positions
        stocks (list): list of dictionaries containing stocks and their current
        prices
        exchange_rate (float): rate at which stocks of first company will be
        exchanged for stocks of second company.
        margin_interest (float): yearly interest charge for margin purchase and
        short sales.
        commission (float): cost per buy and sell order from broker
        position_size(float): amount of money to wager in trade
        initial_margin(float): initial margin percentage

    Returns:
        float: number representing value of spread. Can be negative if the
        current rate is close enough to the final exchange rate that the margin
        interest rate is greater, or if the quantity traded is low enough for
        commission to significantly affect expected return.
    """
    # TODO: Eventually account for the fact I assume you can buy fractions
    # TODO: of a share
    # Leveraged position size
    buying_power = position_size / initial_margin - commission * 2
    current_rate = stocks[0]['Price'] / stocks[1]['Price']
    if current_rate > exchange_rate:  # First stock trading at premium
        stocks[0]['Action'] = 'Long'
        stocks[1]['Action'] = 'Short'
    else:
        stocks[1]['Action'] = 'Long'
        stocks[1]['Action'] = 'Short'
    for stock in stocks:
        if stock['Action'] == 'Long':
            long_weight = exchange_rate
            total_long_value = buying_power * long_weight
            long_loan = total_long_value - position_size * long_weight
            long_interest = long_loan * (1 + margin_interest)**(days/365)
            # long_quantity = long_value / stock['Price']  # Shares to buy
        if stock['Action'] == 'Short':
            total_short_value = buying_power - total_long_value
            short_loan = total_short_value - position_size * (1 - long_weight)
            short_interest = short_loan * (1 + margin_interest)**(days/365)
            # short_quantity = total_short_value / stock['Price']
    total_interest = long_interest + short_interest
    total_pmts = total_interest + commission  # Pay commission exit positions
    total_gain = total_short_value - total_long_value - total_pmts
    return total_gain


def margin_call_long(price: float, initial_margin: float,
                     maintenance_margin: float) -> float:
    """Calculates the margin call price of holding a security based on its
    initial price, it's initial margin requirement, and its maintenance margin
    requirement.

    Args:
        price (float): price in $/share of the security
        initial_margin (float): percentage (typically 40%) of the total
        value of the trade which must be paid for by the investor
        maintenance_margin (float): percentage requirement (typically 20%) of
        the value of the trade which the initial margin posted must exceed.

    Returns:
        float: share price below which a margin call is triggered and the
        investor must post additional margin or the brokerage will unwind their
        positions.
    """
    if price <= 0:
        raise ValueError("Stock price can't be negative")
    if initial_margin <= 0:
        raise ZeroDivisionError("Initial margin can't be zero")
    if maintenance_margin <= 0:
        raise ZeroDivisionError("Maintenance margin can't be zero")
    if initial_margin < maintenance_margin:
        raise ZeroDivisionError("Maintenance margin can't be greater than" +
                                " initial margin")
    margin_call_price = (price * (1 - initial_margin) /
                         (1 - maintenance_margin))
    return margin_call_price


# def get_prices(tickers: list)->list:
#     """Returns the most recent stock price"""
#     get_prices = []
#     for t in tickers:
#         tkr = yf.YahooFinancials(t)
#         data = tkr.get_stock_price_data()[t]
#         get_prices.append([t, data['regularMarketPrice']])
#     return get_prices


# def add_to_db(db_file, tickers):
#     """Adds the scraped tickers to the database and calculates positions"""
#     now = datetime.now()
#     prices = get_prices(tickers)
#     conn = create_connection(db_file)
#     db = conn.cursor()
#     # Add the price to the database and determine the holding period return
#     for price in prices:
#         ticker = price[0]
#         value = price[1]
#         db.execute('SELECT price FROM aemklg WHERE Ticker = ? ORDER BY'
#                    'DateTime DESC LIMIT 1;')


# def create_connection(db_file):
#     """ create a database connection to a SQLite database """
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         return conn
#     except Error as e:
#         print(e)
