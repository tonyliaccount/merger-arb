"""This module contains the code for scraping Junior Mining Network.
Its usage is for the scrape() function to be called periodically, given
one or more topics and a start date"""

import urllib.request
import json
from datetime import datetime

def scrape(topics: list, start_date: str) -> list:
    """This function takes in one or more topics a start date and
    returns titles and timestamps for each article in that topic."""
    url = 'https://www.juniorminingnetwork.com/mining-topics/topic/'
    articles = []
    for topic in topics:
        exceeded_start_date = False
        page_number = 1
        r_url = (url + topic + '?&page=' + str(page_number)
                 + "&format=json")
        # Is there content on the page?
        content_on_page = check_page(r_url)
        # Continue running script until there's no content.
        while content_on_page:
            articles.extend(gather_articles(r_url, start_date))
            page_number += 1
            # Now check if the next page has content
            content_on_page = check_page(r_url)
            r_url = (url + topic + '?&page=' + str(page_number)
                     + "&format=json")
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
                                         "%y/%m/%d %H:%M:%S")
        if article_date > start_date:
            articles.append({"Date":article['publish_up'], "Title": article['title']})
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
        if article['Date'] <= start_date:
            return True
    return False
