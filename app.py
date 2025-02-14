from flask import Flask, render_template, jsonify
import json
from config import DEALS_JSON_PATH

app = Flask(__name__)

# Load deals from JSON file
def load_deals():
    try:
        with open(DEALS_JSON_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

@app.route('/')
def home():
    deals = load_deals()
    return render_template("index.html", deals=deals)

@app.route('/api/deals')
def api_deals():
    return jsonify(load_deals())

if __name__ == "__main__":
    app.run(debug=True)
