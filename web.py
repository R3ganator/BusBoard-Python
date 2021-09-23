from flask import Flask, render_template, request
from main import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/busInfo")
def busInfo():
    stops = []
    postcode = request.args.get('postcode')
    while True:
        try:
            check(postcode)
            break
        except ValueError:
            return render_template('info.html', postcode=postcode + ' which is invalid.', stops=[])
    atcocode = get_atcocode(postcode)
    for i in atcocode:
        stops.append(getTimetable(i))

    return render_template('info.html', postcode=postcode, stops=stops)

if __name__ == "__main__": app.run()