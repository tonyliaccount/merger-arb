from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error
import atexit
import scrape
import spacy_nlp

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape_to_db, trigger="interval", days=7)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

# Try and connect to the database
connect_to_db('deals.db')

@app.route("/")
def index():
    deals = db.execute("SELECT * FROM financings;")
    return render_template("index.html", deals=deals)


def scrape_to_db():
    # Create a list of the financing headlines
    ents = scrape.scrape("financing")
    # Process the list using Spacy
    deals = spacy_nlp.name_and_amount(ents)
    # Add missing deals into the database
    for d in deals:
        db.execute("INSERT INTO financings(Datetime, Title, Borrower"
                   + "Amount) VALUES(?,?,?,?);", d[0], d[1], d[2], d[3])


def connect_to_db(db_path):
    """ Create database connection to file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
