"""This module contains a function that will extract junior miners and
amounts from the titles by using spacy's NER and amount tools"""

import spacy

nlp = spacy.load("en_core_web_sm")


def name_and_amount(scraped_list:list) -> list:
    names_list = []
    for line in scraped_list:
        # Process the title
        doc = nlp(line[0])
        for ent in doc.ents():
            # Is there at least one 
            # Extract the first ORG (junior miner) from text
            company = nlp
            # Optional: Extract the first MONEY
            # Add the date, company, and amt to the list
            names_list.append([line[0], company, amount])
    return names_list
