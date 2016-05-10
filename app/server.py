import bottle
from bottle import route, run, template, static_file
from bottle.ext import sqlite
import datetime

app = bottle.Bottle()
plugin = sqlite.Plugin(dbfile='./db/test.db')
app.install(plugin)

# Show the line chart.
@app.route('/')
def index(db):
    return template('template/chart')

# Output csv file.
@app.route('/data.csv')
def data(db):
    lines = []
    lines.append('date,temperature')

    # Query database, only show the last 60 entries.
    rows = db.execute('SELECT `date`, `temperature` FROM `stats` ORDER BY `date` DESC LIMIT 60;').fetchall()
    for row in rows:
        date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").isoformat()
        temp = str(row[1])
        lines.append(date + ',' + temp)

    # Concat all lines to csv format..
    return '\n'.join(lines)

# Static file, e.g. javascript...
@app.route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static')

# Server start.
app.run(host='0.0.0.0', port=3000, debug=True)
