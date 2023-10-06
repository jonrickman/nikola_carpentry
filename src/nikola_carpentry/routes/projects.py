from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from nikola_carpentry import app, LoginForm, ReviewForm, db
from nikola_carpentry.models import AdminUser, Review

@app.route("/projects", methods=["GET", "POST"])
def projects():
    return render_template("projects.html")