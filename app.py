from flask import Flask, request, send_from_directory, redirect, jsonify
from main import runNewClueGenerator
from scraper import runScraper


app = Flask(__name__, static_folder='public')


@app.route('/')
def hello():
    return redirect("/index.html", code=302)


@app.route('/<path:path>')
def root(path):
    return send_from_directory('public', path)


@app.route("/newClues")
def newClues():
    date = request.args.get('date')
    print("Puzzle downloading started")
    # runScraper()
    print("Puzzle downloading finished")
    result = runNewClueGenerator(date)
    return jsonify(result)


if __name__ == '__main__':
    app.run()
