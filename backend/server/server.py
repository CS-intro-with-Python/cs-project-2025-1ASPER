import os
from flask import Flask, jsonify, render_template
from .services import recommendation_service

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '../templates')


app = Flask(__name__, template_folder=TEMPLATE_DIR)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/recommendations")
def get_recommendations():
    return jsonify(recommendation_service.get_recommendations())