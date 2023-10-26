from flask import render_template
from nikola_carpentry import app


@app.route("/403.html")
def HTTP403():
    return render_template("403.html")


@app.route("/404.html")
def HTTP404():
    return render_template("404.html")