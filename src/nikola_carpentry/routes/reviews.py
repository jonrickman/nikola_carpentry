from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user

from nikola_carpentry import ReviewForm, db
from nikola_carpentry.app import app
from nikola_carpentry.models import Review


@app.route("/reviews", methods=["GET", "POST"])
def review_home():
    reviews = Review.query.filter_by(approved=True).all()

    average_rating = 5

    if len(reviews) > 0:
        average_rating = round(sum([r.rating for r in reviews]) / len(reviews), 2)

    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(
            author=form.author.data,
            rating=form.rating.data,
            title=form.title.data,
            content=form.content.data,
        )

        with app.app_context():
            review.insert()

        flash("Review created successfully. Review must be approved before it appears.")
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("review_home"))

    return render_template(
        "reviews.html",
        user=current_user,
        reviews=reviews,
        form=form,
        average_rating=average_rating,
    )


@app.route("/reviews/<int:review_id>/")
def get_review(review_id: int):
    review = Review.query.filter_by(id=review_id).first()
    form = ReviewForm()

    return render_template("review.html", user=current_user, form=form, review=review)


@app.route("/reviews/filter/<int:rating>")
def filter_reviews(rating: int):
    if rating:
        reviews = Review.query.filter(Review.rating == rating).all()
        return render_template("review-pane.html", reviews=reviews)

    reviews = Review.query.filter().all()
    return render_template("review-pane.html", reviews=reviews)


@app.route("/reviews/approve/<int:review_id>/")
def approve_review(review_id: int):
    Review.query.filter_by(id=review_id).update({"approved": True})

    if current_user.is_authenticated:
        db.session.commit()
        return redirect(url_for("review_home"))

    return "Nope"


@app.route("/reviews/delete/<int:review_id>/")
def delete_review(review_id: int):
    Review.query.filter_by(id=review_id).delete()

    if current_user.is_authenticated:
        db.session.commit()
        return redirect(url_for("review_home"))

    return "Nope"
