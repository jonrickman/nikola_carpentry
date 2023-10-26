from flask import render_template, flash
from nikola_carpentry import app


@app.route("/")
def home():
    flash("BRB")
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")