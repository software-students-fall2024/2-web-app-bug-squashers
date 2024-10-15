import os
from flask import Flask, render_template, make_response, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import pytz

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
        # response = make_response("Test", 200)
        # response.mimetype = "text/plain"
        return render_template("base.html")
    

    @app.route("/add", methods = ["GET"])
    def render_add():
        return render_template("add-task.html")
    
    @app.route("/add", methods=["POST"])
    def submit_add():
        quickinfo = request.form.get("task_title")
        additionalinfo = request.form.get("user_message")
        duedate = request.form.get("date")

        if not quickinfo or not additionalinfo or not duedate:
            return render_template("add-task.html", error ="All fields are required!")
        
        try:
            due_date = datetime.strptime(duedate, "%Y-%m-%d")
        except ValueError:
            return render_template("add-task.html", error="Invalid date format. Use YYYY-MM-DD.")

        est = pytz.timezone('America/New_York')
        current = datetime.now(est)

        new_entry = {
            "completed": False,
            "quickinfo": quickinfo,
            "additionalinfo": additionalinfo,
            "date": current,
            "duedate": duedate
            
        }

        result = collection.insert_one(new_entry)
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