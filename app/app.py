import os
from flask import Flask, render_template, make_response, request, redirect, url_for

def create_app():

    app = Flask(__name__)

    @app.route("/")
    def home():
        response = make_response("Test", 200)
        response.mimetype = "text/plain"
        return response
    

    @app.route("/add")
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