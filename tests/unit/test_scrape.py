import scrape
from datetime import datetime


def test_scrape():
    """Check that given a topic and start date, that the function returns
    a list object """
    date = datetime.now()
    topics = ["financings"]
    articles = scrape(topics, start_date=date)
    assert(isinstance(articles, list))


def test_gather_articles():
    # TODO: Mock a urllib response object with a JSON fixture
    # TODO: Check that the returned list is the same as the fixture
    pass


def test_page_check_with_content():
    # TODO: Mock a urllib respose object with a JSON fixture representing
    # TODO: content. Assert that check_page returns True.
    pass


def test_page_check_without_content():
    # TODO: Mock a urllib respose object with a JSON fixture representing
    # TODO: check page without content. Assert that check_page returns False.
    pass


def test_up_to_date_true():
    # TODO: Pass in a list of articles and ensure that 
    pass


def test_up_to_date():
    pass


def test_identify_company():
    pass


def test_earliest_matches():
    pass
