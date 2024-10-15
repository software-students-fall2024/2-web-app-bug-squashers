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
        quick_info = request.form.get("task_title")
        additional_info = request.form.get("user_message")
        due_date = request.form.get("date")

        if not quick_info or not additional_info or not due_date:
            return render_template("add-task.html", error ="All fields are required!")
        
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return render_template("add-task.html", error="Invalid date format. Use YYYY-MM-DD.")

        est = pytz.timezone('America/New_York')
        current = datetime.now(est)

        new_entry = {
            "completed": False,
            "quick_info": quick_info,
            "additional_info": additional_info,
            "date": current,
            "due_date": due_date
            
        }

        result = collection.insert_one(new_entry)
        return redirect(url_for("home"))

    @app.route("/edit")
    def edit():
        return redirect(url_for("home"))


    @app.route("/search", methods = ["GET"])
    def search():
        query = request.args.get("query")

        if query:
            tasks = collection.find({"quickinfo": {"$regex": f".*{query}.*", "$options": "i"}}) 
            results = list(tasks)
            return render_template("search-results.html", tasks=results, query=query)
        else:
            results = []

        return render_template("search.html")
    
    @app.route("/tasklist")
    def tasklist():
        return render_template("task-list.html")

    # @app.route("/task-list")
    # def load_list():
    #     return render_template('/task-list.html', task_list=collection)

    return app

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app = create_app()
    app.run(port=FLASK_PORT)