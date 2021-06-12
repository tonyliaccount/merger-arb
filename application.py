from flask import Flask, render_template, request
import atexit
import scrape
import spacy_helpers
import sqlite_helpers
#from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# app = Flask(__name__)

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=sqh.scrape_to_db, trigger="interval", minutes=15)
# scheduler.start()
# atexit.register(lambda: scheduler.shutdown())
conn = sqlite_helpers.create_connection('deals.db')


# @app.route("/")
# def index():
#     db = conn.cursor()
#     deals = db.execute("SELECT * FROM financings;")
#     conn.commit()
#     return render_template("index.html", deals=deals)


def scrape_to_db():
    db = conn.cursor()
    # Determine the latest date in the database so we can start scraping after.
    start_date = db.execute("SELECT DateTime FROM financings ORDER BY DateTime"
                            + " DESC LIMIT 1;").fetchall()
    # Then format it
    start_date = datetime.strptime(start_date[0][0], "%Y-%m-%d %H:%M:%S")
    # Create a list of the financing headlines
    deals = scrape.scrape(["financing"], start_date)
    # Add new deals into the database
    for d in deals:
        db.execute("INSERT INTO financings(Datetime, Title, Borrower"
                   + "Amount) VALUES(?,?,?,?);", d[0], d[1], d[2], d[3])
    conn.commit()

scrape_to_db()
