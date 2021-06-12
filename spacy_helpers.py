"""This module contains a function that will extract junior miners and
amounts from the titles by using spacy's NER and amount tools"""

import spacy

nlp = spacy.load("en_core_web_sm")


def extract_money(scraped_list:list) -> list:
    """Returns the first monetary value present in a list of headlines"""
    names_list = []
    for line in scraped_list:
        # Process the title
        doc = nlp(line[1])
        amount = None
        for ent in doc.ents:
            if ent.label_ == "MONEY" and amount is None:
                amount = ent.text
        names_list.append([line[1], amount])
    return names_list
