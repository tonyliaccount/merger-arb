"""This module contains the code for scraping Junior Mining Network.
Its usage is for the scrape() function to be called periodically, given
some tags """

import urllib.request
import json


def scrape(topics: list) -> list:
    """This function takes in one or more topics and returns titles and
    timestamps for each article in that topic."""
    url = 'https://www.juniorminingnetwork.com/mining-topics/topic/'
    articles = [["Title", "Timestamp"]]
    page_content = True
    for topic in topics:
        page_number = 1
        r_url = (url + topic + '?&page=' + str(page_number)
                 + "&format=json")
        while page_content:
            add_articles(r_url, articles)
            page_number += 1
            # Now check if the next page has content
            page_content = check_page(r_url)
            r_url = (url + topic + '?&page=' + str(page_number)
                     + "&format=json")
    return articles


def add_articles(r_url: str, articles: list):
    """This function adds all articles on a page to the list."""
    response = urllib.request.urlopen(r_url)
    content = response.read()
    json_content = json.loads(content)
    if check_page(r_url):
        for article in json_content['articles']:
            articles.append(article['publish_up'], [article['title']])


def check_page(r_url: str) -> bool:
    """Determine if there is some content on this page"""
    response = urllib.request.urlopen(r_url)
    content = response.read()
    json_content = json.loads(content)
    if json_content['articles'] != []:
        return True
    else:
        return False
