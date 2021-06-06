"""This module populates the database with the start articles. 
This is useful because I won't have to waste Heroku compute on collecting
data which I can do on my local machine. Once its written, delete it."""

import os
import json
import sqlite3
import spacy_nlp
from sqlite3 import Error


def main():
    conn = create_connection('deals.db')
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS financings(
                                        id integer PRIMARY KEY,
                                        DateTime text NOT NULL,
                                        Title text NOT NULL,
                                        Borrower text NOT NULL,
                                        Amount float
                                    ); """
    if conn is not None:
        create_table(conn, sql_create_projects_table)
    fp = r'C:\Users\Adam\OneDrive\HSA\Resources\JuniorMiningNetwork\Financing'
    j_list = json_to_list(fp)
    cur = conn.cursor()
    list_to_db(cur, j_list)



def json_to_list(fp: str) -> list:
    """ Takes a filepath to a directory, and then extracts all titles 
    and publish dates from each article"""
    j_list = []
    for f in os.listdir(fp):
        if f.endswith('.json'):
            json_raw = open(os.path.join(fp, f))
            json_read = json_raw.read()
            json_obj = json.loads(json_read)
            for article in json_obj['articles']:
                j_list.append([article['publish_up'], article['title']])
    return j_list

def list_to_db(db, articles: list):
    # Process the list using Spacy
    deals = spacy_nlp.name_and_amount(articles)
    # Add missing deals into the database
    for d in deals:
        data_tuple = (d[0], d[1], d[2], d[3])
        db.execute("INSERT INTO financings(Datetime, Title, Borrower"
                   + "Amount) VALUES(?,?,?,?);", data_tuple)
        db.commit()
    db.close()

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

if __name__ == "__main__":
    main()