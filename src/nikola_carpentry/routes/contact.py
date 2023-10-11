from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from nikola_carpentry.app import app
from nikola_carpentry import ContactForm, db, send_contact_email
from nikola_carpentry.models import Contact


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        subject = form.subject.data
        contact_name = form.contact_name.data
        email = form.email.data
        phone = form.phone.data
        content = form.content.data

        contact = Contact(
            subject=subject, contact_name=contact_name, email=email, phone=phone, content=content
        )

        send_contact_email(contact)
        flash("Review created successfully. Review must be approved before it appears.")
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("contact"))

    return render_template(
        "contact.html",
        user=current_user,
        form=form,
    )
