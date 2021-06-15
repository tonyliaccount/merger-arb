import sqlite3
from sqlite3 import Error
import spacy
from forex_python.converter import CurrencyRates
import datetime
import re


nlp = spacy.load("en_core_web_sm")


def extract_money(text: str) -> str:
    """Returns the first monetary value present in a list of headlines"""
    # Process the headline
    doc = nlp(text)
    amount = None
    for ent in doc.ents:
        if ent.label_ == "MONEY" and amount is None:
            amount = ent.text
    return amount


def format_currency(currency: str, date: datetime.datetime) -> float:
    """Converts a string representing a currency to a float representing
    dollars."""
    currency = str(currency)
    # Commas removed because they impact decimal regex
    remove_commas = currency.replace(",", "")
    # Is the Value in USD?
    is_USD = True if "US" in currency else False
    # Determine if Million or Billion are used in headline
    regex_M = r"\d+ ?([mM]|[mM]illion)"
    match_M = re.search(regex_M, currency)
    is_M = True if match_M is not None else False
    regex_B = r"\d+ ?([bB]|[bB]illion)"
    match_B = re.search(regex_B, currency)
    is_B = True if match_B is not None and is_M is None else False
    regex_d = r"\d+\.?\d?\d?"
    amt_match = re.search(regex_d, remove_commas)
    if amt_match is not None:
        amount = float(amt_match.group(0))
    # Convert to CAD if applicable
        if is_USD is True:
            amount *= USD_CAD_rate(date)
        if is_M is True:
            amount *= 1000000
        elif is_B is True:
            amount *= 1000000000
        return amount
    return None


def USD_CAD_rate(date: datetime.datetime) -> float:
    """Converts a value in USD to equivalent CAD given a date"""
    # ToDo: Figure out why this isn't working
    # c = CurrencyRates()
    #rate = c.get_rate('USD', 'CAD', date)
    rate = 1.3
    return rate


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


# def create_table(conn, create_table_sql):
#     # Does this need to be here?
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)


# def list_to_db(db, articles: list):
#     # Does this need to be here?
#     # Process the list using Spacy
#     deals = spacy_nlp.name_and_amount(articles)
#     # Add missing deals into the database
#     for d in deals:
#         data_tuple = (d[0], d[1], d[2], d[3])
#         db.execute("INSERT INTO financings(Datetime, Title, Borrower,"
#                    + "Amount) VALUES(?,?,?,?);", data_tuple)


# conn = create_connection('deals.db')
# fp = r'C:\Users\Adam\OneDrive\HSA\Resources\JuniorMiningNetwork\Financing'
# j_list = json_to_list(fp)
# cur = conn.cursor()
# list_to_db(cur, j_list)
# conn.commit()
# conn.close()