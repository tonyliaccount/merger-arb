from flask import Flask, render_template, request
import atexit
import scrape
import helpers
from apscheduler.schedulers.background import BackgroundScheduler

# Configure application
app = Flask(__name__)
app.debug = False
# Create a periodic job to scrape new financing activities
scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape.scrape_to_db, trigger="interval", minutes=1)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def index():
    conn = helpers.create_connection('deals.db')
    db = conn.cursor()
    deals = db.execute("SELECT DateTime, Title, Borrower, Amount FROM" +
                       " financings ORDER BY DateTime DESC LIMIT 50;")
    conn.commit()
    return render_template("index.html", deals=deals)


@app.template_filter('strftime')
def _jinja2_filter_datetime(value):
    return value[:-9]


@app.template_filter('fmt_money')
def _jinja2_filter_money(value):
    return '{:-9,.1f}'.format(value/1000000)
