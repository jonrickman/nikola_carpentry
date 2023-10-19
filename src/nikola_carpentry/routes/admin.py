from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
from werkzeug.security import check_password_hash
from nikola_carpentry import app, db, LoginForm, UserForm, TagForm
from nikola_carpentry.models import AdminUser, Tag

basicAuth = HTTPBasicAuth()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@login_required
@app.route("/admin", methods=["GET", "POST"])
def admin_home():
    # TODO: Cleanup this method...
    if not current_user.is_authenticated:
        return render_template("403.html")

    user_form = UserForm()
    tag_form = TagForm()
    users = AdminUser.query.filter().all()
    tags = Tag.query.filter().all()

    if user_form.validate_on_submit():
        form_username = user_form.username.data.lower()
        form_email = user_form.email.data.lower()

        # see if user exists with given username
        user: AdminUser = AdminUser.query.filter_by(username=form_username).first()
        if user:
            # if user exists, flash error and return
            flash(f"User with {form_username} already exists", "danger")
            return render_template(
                "admin.html",
                tag_form=tag_form,
                user_form=user_form,
                user=current_user,
                users=users,
                tags=tags,
            )
        # otherwise create the user
        user = AdminUser(
            username=form_username, password=user_form.password.data, email=form_email
        )
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        # flash the message and return
        flash("User created succesfully")
        return redirect(url_for("admin_home"))

    if tag_form.validate_on_submit():
        form_tag_name = tag_form.tag_name.data.lower()

        tag: Tag = Tag.query.filter_by(tag_name=form_tag_name).first()
        # see if user exists with given username
        if tag:
            # if user exists, flash error and return
            flash(f"Tag with {form_tag_name} already exists", "danger")
            return render_template(
                "admin.html",
                tag_form=tag_form,
                user_form=user_form,
                user=current_user,
                users=users,
                tags=tags,
            )

        # otherwise create the user
        tag = Tag(tag_name=form_tag_name)
        with app.app_context():
            db.session.add(tag)
            db.session.commit()

        # flash the message and return
        flash("User created succesfully")
        return redirect(url_for("admin_home"))

    return render_template(
        "admin.html",
        tag_form=tag_form,
        user_form=user_form,
        user=current_user,
        users=users,
        tags=tags,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin_home"))

    form = LoginForm()
    if form.validate_on_submit():
        # find the user -- cast to lower
        form_username = form.username.data.lower()
        user: AdminUser = AdminUser.query.filter_by(username=form_username).first()

        # check if user found and validate the password hash
        if user and check_password_hash(user.password_hash, form.password.data):
            # login user
            login_user(user, remember=form.remember.data)

            # update last_updated
            AdminUser.query.filter_by(id=user.id).update(
                {"time_updated": datetime.now()}
            )
            db.session.commit()

            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")

    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!  Thanks For Stopping By...")
    return redirect(url_for("login"))
