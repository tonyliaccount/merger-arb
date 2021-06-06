"""This module contains a function that will extract junior miners and
amounts from the titles by using spacy's NER and amount tools"""

import spacy

nlp = spacy.load("en_core_web_sm")


def name_and_amount(scraped_list:list) -> list:
    names_list = []
    for line in scraped_list:
        # Process the title
        doc = nlp(line[1])
        company = None
        amount = None
        for ent in doc.ents:
            if ent.label_ == "MONEY" and amount is None:
                amount = ent.text
            if ent.label_ == "ORG" and company is None: 
                company = ent.text
            # Add the date, company, and amt to the list
        names_list.append([line[0], line[1], company, amount])
    return names_list
