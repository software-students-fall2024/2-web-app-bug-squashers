import os
from flask import Flask, render_template, make_response, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def create_app():

    app = Flask(__name__)

    MONGO_URI = os.getenv("MONGO_URI")

    if MONGO_URI is None:
        raise ValueError("Error with URI")
    
    try:
        client = MongoClient(MONGO_URI)
        db = client.get_database("Planner")
        collection = db["entries"]
        print("Connected")
    except Exception as e:
        print(f"Error: {e}")

    @app.route("/")
    def home():
        response = make_response("Test", 200)
        response.mimetype = "text/plain"
        return response
    

    @app.route("/add", methods = ["POST"])
    def add():
        return redirect(url_for("home"))
    

    @app.route("/edit")
    def edit():
        return redirect(url_for("home"))


    @app.route("/search")
    def search():
        return redirect(url_for("home"))


    return app

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app = create_app()
    app.run(port=FLASK_PORT)