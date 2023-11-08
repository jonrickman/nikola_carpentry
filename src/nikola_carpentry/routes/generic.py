from flask import flash, render_template

from nikola_carpentry import app


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/flash")
def flash_message():
    flash("Test message 1")
    flash("Test message 2")
    flash("Test message 3")

    return render_template("index.html")
