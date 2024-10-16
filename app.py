import os
import pytz
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from bson.objectid import ObjectId
from flask import Flask, render_template, make_response, request, redirect, url_for

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
        return render_template("base.html")
    
    @app.route("/add", methods = ["GET"])
    def render_add():
        return render_template("add-task.html")
    
    @app.route("/add", methods=["POST"])
    def submit_add():
        name = request.form.get("task_title")
        desc = request.form.get("user_message")
        due_date = request.form.get("date")

        if not name or not desc or not due_date:
            return render_template("add-task.html", error ="All fields are required!")
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return render_template("add-task.html", error="Invalid date format. Use YYYY-MM-DD.")

        new_entry = {
            "name": name,
            "description": desc,
            "due_date": due_date
        }

        collection.insert_one(new_entry)
        return redirect(url_for("tasklist"))

    @app.route("/edit/<id>")
    def render_edit(id):
        doc = collection.find_one({"_id": ObjectId(id)})
        return render_template("edit-task.html", doc=doc)

    @app.route("/edit/<id>", methods=["POST"])
    def submit_edit(id):
        vals = {
            "name": request.form["name"],
            "description": request.form["desc"],
            "due_date": request.form["due_date"]
        }
        collection.update_one({"_id": ObjectId(id)}, {"$set": vals})
        return redirect(url_for("tasklist"))

    @app.route("/complete/<id>")
    def render_confirmation(id):
        doc = collection.find_one({"_id": ObjectId(id)})
        return render_template("confirm.html", doc=doc)
    
    @app.route("/complete/<id>", methods=["POST"])
    def mark_complete(id):
        collection.delete_one({"_id": ObjectId(id)})
        return redirect(url_for("tasklist"))

    @app.route("/search")
    def search():
        query = request.args.get("query")

        if query:
            tasks = collection.find({"name": {"$regex": f".*{query}.*", "$options": "i"}}) 
            results = list(tasks)
            return render_template("search-results.html", tasks=results, query=query)
        else:
            results = []

        return render_template("search.html")
    
    @app.route("/tasklist")
    def tasklist():
        tasks = collection.find().sort("due_date", 1)
        tasklist = list(tasks)
        return render_template("task-list.html", tasks=tasklist)

    # @app.route("/task-list")
    # def load_list():
    # return render_template('/task-list.html', task_list=collection)

    return app

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app = create_app()
    app.run(port=FLASK_PORT)