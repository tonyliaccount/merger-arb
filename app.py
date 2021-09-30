from flask import Flask, render_template, request
import atexit
import scrape
import helpers
from apscheduler.schedulers.background import BackgroundScheduler

# Configure application
app = Flask(__name__)
app.debug = False
# Create a periodic job to scrape latest stock prices
scheduler = BackgroundScheduler()
scheduler.add_job(func=helpers.add_to_db(short = 'KLG.TO', long = 'AEM.TO'),
                  trigger="interval", days=1)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def index():
    conn = helpers.create_connection('positions.db')
    db = conn.cursor()
    deals = db.execute("SELECT DateTime, Ticker, Return, Margin Interest Pmts FROM" +
                       " AEMKLG ORDER BY DateTime;")
    conn.commit()
    # TODO: Format this so it can be plotted easily
    return render_template("index.html", positions=positions)


@app.template_filter('strftime')
def _jinja2_filter_datetime(value):
    return value[:-9]


@app.template_filter('fmt_money')
def _jinja2_filter_money(value):
    return '{:-9,.1f}'.format(value/1000000)
