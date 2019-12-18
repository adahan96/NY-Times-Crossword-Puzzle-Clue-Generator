from flask import Flask, request, send_from_directory, redirect, jsonify
from main import runNewClueGenerator

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
    result = runNewClueGenerator(date)
    return jsonify(result)


if __name__ == '__main__':
    app.run()
