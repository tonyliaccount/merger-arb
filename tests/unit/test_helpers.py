from datetime import datetime
import helpers


def test_spacy_extracts_amount():
    """ Spacy handles a valid MONEY entity in the string"""
    string = ('Major Precious Metals Announces C$10,000,000 Non-Brokered'
          ' Private Placement')
    assert(helpers.extract_money(string) == "10,000,000")


def test_spacy_no_money():
    """ When there is no MONEY entity, Spacy returns None"""
    string = ('Fortune Minerals Closes Private Placement for Working Capital'
              ' and Receives Government Grant to Support Drilling')
    assert(helpers.extract_money(string) is None)


def test_spacy_handles_multiple():
    """ When there are multiple valid amounts, function returns only first"""
    string = ("CITIC Metal's C$612 Million (US$465 Million) Second Equity"
              " Investment in Ivanhoe Mines to Close August 16, 2019."
              " Additional C$67 Million (US$51 Million) to Be Received"
              " Concurrently from Zijin Mining")
    assert(helpers.extract_money(string) == "C$612 Million")


def test_currency_formatting_no_suffix():
    """ Converts an amount string found by Spacy to a float"""
    date = datetime(2021, 1, 1, 0, 0, 0)
    string = "10,000,000"
    assert(helpers.format_currency(string, date) == 10000000)


def test_currency_formatting_letter_suffix():
    """ Converts an amount string found by Spacy to a float, where the string
    include a letter (either [mM] or [bB])."""
    date = datetime(2021, 1, 1, 0, 0, 0)
    string = "C$612 Million"
    assert(helpers.format_currency(string, date) == 612000000)


def test_CAD_USD_conversion():
    """ Converts a string containing a US figure into CAD """
    # TODO: Ensure that the
    # TODO: add a string with a US figure
    # TODO: assert that the resulting conversion is correct
