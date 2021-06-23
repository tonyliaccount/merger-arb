from flask import Flask, render_template
import scrape
import helpers
from apscheduler.schedulers.background import BlockingScheduler

# Configure application
app = Flask(__name__)

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def update():
    scrape.scrape_to_db()

sched.start()


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
