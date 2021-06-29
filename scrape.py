"""This module contains the code for scraping Junior Mining Network.
Its usage is for the scrape() function to be called periodically, given
one or more topics and a start date"""

from datetime import datetime
import helpers
import requests
from fake_useragent import UserAgent
from itertools import cycle
import logging
import os
import http.client as http_client

ua = UserAgent()
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
http_client.HTTPConnection.debuglevel = 1

# proxyDict = {
#               "http"  : os.environ.get('FIXIE_URL', ''),
#               "https" : os.environ.get('FIXIE_URL', '')
#             }
            
def scrape(topics: list, start_date: str) -> list:
    """This function takes in one or more topics a start date and
    returns titles and timestamps for each article in that topic."""
    url = 'https://www.juniorminingnetwork.com/mining-topics/topic/'
    articles = []
    # Leaving the door open in case I ever want to include multiple topics
    for topic in topics:
        # Start at the most recent content
        page_number = 1
        r_url = (url + topic + '?&page=' + str(page_number)
                 + "&format=json")
        # Is there content on the page?
        content_on_page = valid_page(r_url)
        # Continue running script until there's no content.
        while content_on_page:
            # Poll Junior Mining Network for more articles
            articles.extend(gather_articles(r_url, start_date))
            page_number += 1
            r_url = url + topic + '?&page=' + str(page_number) + "&format=json"
            # Check if the next page has content
            content_on_page = valid_page(r_url)
            # Check whether the start date has been reached
            if is_last_page(r_url, start_date):
                return articles
    return articles


def scrape_to_db():
    """Calls scrape function and adds its results to the database"""
    conn = helpers.create_connection('deals.db')
    db = conn.cursor()
    # Get the last date in the database so we can start scraping after.
    start_date = db.execute("SELECT DateTime FROM financings ORDER BY DateTime"
                            + " DESC LIMIT 1;").fetchall()
    start_date = datetime.strptime(start_date[0][0], "%Y-%m-%d %H:%M:%S")
    # Create a list of the latest headlines
    deals = scrape(["financing"], start_date)
    # Add new deals into the database
    for d in deals:
        db.execute("INSERT INTO financings(Datetime, Title, Borrower,"
                   + "Amount) VALUES(?,?,?,?);",
                   (d["Date"], d["Title"], d["Borrower"], d["Amount"]))
    conn.commit()


def gather_articles(r_url: str, start_date: str):
    """Given a web url, add all articles up to a certain date."""
    articles = []
    r = requests.get(r_url,
                     headers={"headers": ua.random},
                     )
    json_content = r.json()
    for article in json_content['articles']:
        article_date = datetime.strptime(article['publish_up'],
                                         "%Y-%m-%d %H:%M:%S")
        # Stop once the old articles are reached
        if article_date > start_date:
            # Figure out who the company is
            amount = helpers.extract_money(article["title"])
            formatted_amount = helpers.format_currency(amount, article_date)
            company = identify_company(article['title'])
            if formatted_amount is not None and company is not None:
                articles.append({
                                "Date": article['publish_up'],
                                "Title": article['title'],
                                "Borrower": company,
                                "Amount": formatted_amount,
                                })
    return articles


def valid_page(r_url: str) -> bool:
    """Determine if there is some content on this page"""
    print(f"The url passed to valid_page was {r_url}, proxy was NA")
    r = requests.get(r_url,
                     headers={"headers": ua.random},
                     )
    h = r.request.headers
    print(h)
    json_content = r.json()
    if json_content['articles'] != []:
        return True
    else:
        return False


def is_last_page(r_url: str, start_date: datetime) -> bool:
    """Checks if a page contains an article with a date after the start date"""
    # response = urllib.request.urlopen(r_url)
    print(f"The url passed to is_last_page was {r_url}, proxy was NA")
    r = requests.get(r_url,
                     headers={"headers": ua.random},
                     )
    print(f"Is last page got {r}")
    json_content = r.json()
    for article in json_content['articles']:
        article_date = datetime.strptime(article['publish_up'], "%Y-%m-%d %H:%M:%S")
        if article_date <= start_date:
            return True
    return False


def identify_company(headline: str):
    """Given a string, determine which company is being referred to.
    If there are multiple matches, return the longest. If there are no
    matches, return None. If there are multiple companies in the input
    string, only find the first one.Return companies that match any part
    of the query."""
    conn = helpers.create_connection('deals.db')
    db = conn.cursor()
    companies = db.execute("SELECT common_name FROM listings WHERE " +
                           "INSTR(?, common_name) > 0;",
                           (headline,)).fetchall()
    length = len(companies)
    if length > 1:
        first = earliest_matches(companies, headline)
        return max(first, key=len)
    elif length == 1:
        return companies[0][0]
    else:
        return None


def earliest_matches(companies, headline) -> list:
    """ Creates a list of one or more companies that appear at the
    earliest part of the headline. """
    index = None
    for c in companies:
        location = headline.find(c[0])
        if index is None or location < index:
            index = location
            earliest = [c[0]]
        elif location == index:
            earliest.append(c[0])
    return earliest
