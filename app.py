from flask import Flask, render_template, request
import atexit
import scrape
import helpers
#from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import timeit
import pandas as pd

app = Flask(__name__)

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=sqh.scrape_to_db, trigger="interval", minutes=15)
# scheduler.start()
# atexit.register(lambda: scheduler.shutdown())
conn = helpers.create_connection('deals.db')
db = conn.cursor()


@app.route("/")
def index():
    #deals = db.execute("SELECT * FROM financings;")
    #conn.commit()
    #return render_template("index.html", deals=deals)
    #return render_template("index.html")
    return "WOW"


def scrape_to_db():
    # Get the last date in the database so we can start scraping after.
    start_date = db.execute("SELECT DateTime FROM financings ORDER BY DateTime"
                            + " DESC LIMIT 1;").fetchall()
    start_date = datetime.strptime(start_date[0][0], "%Y-%m-%d %H:%M:%S")
    # Create a list of the latest headlines
    deals = scrape.scrape(["financing"], start_date)
    df = pd.read_csv("output.csv")
    deals = df.values.tolist()
    # Add new deals into the database
    for d in deals:
        db.execute("INSERT INTO financings(Datetime, Title, Borrower,"
                   + "Amount) VALUES(?,?,?,?);",
                   (d["Date"], d["Title"], d["Borrower"], d["Amount"]))
    conn.commit()
