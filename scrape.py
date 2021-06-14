"""This module contains the code for scraping Junior Mining Network.
Its usage is for the scrape() function to be called periodically, given
one or more topics and a start date"""

import urllib.request
import json
from datetime import datetime
from helpers import extract_money
import sqlite3

conn = sqlite3.connect('deals.db')
db = conn.cursor()


def scrape(topics: list, start_date: str) -> list:
    """This function takes in one or more topics a start date and
    returns titles and timestamps for each article in that topic."""
    url = 'https://www.juniorminingnetwork.com/mining-topics/topic/'
    articles = []
    for topic in topics:
        # Start at the most recent content
        page_number = 1
        r_url = (url + topic + '?&page=' + str(page_number)
                 + "&format=json")
        # Is there content on the page?
        content_on_page = check_page(r_url)
        # Continue running script until there's no content.
        while content_on_page:
            articles.extend(gather_articles(r_url, start_date))
            page_number += 1
            r_url = (url + topic + '?&page=' + str(page_number)
                     + "&format=json")
            # Check if the next page has content
            content_on_page = check_page(r_url)
            # Check whether the start date has been reached
            if up_to_date(articles, start_date):
                return articles
    return articles


def gather_articles(r_url: str, start_date: str):
    """This function adds all articles on a page up to a certain date."""
    articles = []
    response = urllib.request.urlopen(r_url)
    content = response.read()
    json_content = json.loads(content)
    for article in json_content['articles']:
        article_date = datetime.strptime(article['publish_up'],
                                         "%Y-%m-%d %H:%M:%S")
        # Stop once the old articles are reached
        if article_date > start_date:
            # Figure out who the company is
            amount = extract_money(article["title"])
            company = identify_company(article['title'])
            if amount is not None and company is not None:
                articles.append({
                                "Date": article['publish_up'],
                                "Title": article['title'],
                                "Borrower": company,
                                "Amount": amount,
                                })
    return articles


def check_page(r_url: str) -> bool:
    """Determine if there is some content on this page"""
    response = urllib.request.urlopen(r_url)
    content = response.read()
    json_content = json.loads(content)
    if json_content['articles'] != []:
        return True
    else:
        return False


def up_to_date(articles, start_date):
    """Checks if the articles list is up to date"""
    for article in articles:
        article_date = datetime.strptime(article['Date'], "%Y-%m-%d %H:%M:%S")
        if article_date <= start_date:
            return True
    return False


def identify_company(headline: str):
    """Given a string, determine which company is being
    referred to. If there are multiple matches, return the longest.
    If there are no matches, return None. If there are multiple companies
    in the input string, only find the first one."""
    # Return companies that match any part of the query.
    companies = db.execute("SELECT common_name FROM listings WHERE INSTR(?, common_name) > 0;",
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
