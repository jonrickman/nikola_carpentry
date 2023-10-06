import json 
from nikola_carpentry import db, login_manager, app
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Column, String, Integer, Boolean
from werkzeug.security import generate_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id: int):
    return AdminUser.query.get(int(user_id))


class AdminUser(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, username, password) -> None:
        self.username = username
        password_hash = generate_password_hash(password)
        self.password_hash = password_hash

    def insert(self):
        db.session.add(self)
        db.session.commit()


class Review(db.Model):
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    author = Column(String, nullable=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    posted = Column(DateTime(timezone=True), server_default=func.now())
    image_path = Column(String, nullable=True)
    approved = Column(Boolean, nullable=False, default=False)

    def __init__(self, author, review_title, review_text, approved) -> None:
        self.author = author
        self.title = review_title
        self.content = review_text
        self.approved = approved

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def pretty_date(self) -> str:
        month = self.posted.strftime("%B")
        year = self.posted.strftime("%Y")
        return f"{month} {year}"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


if __name__ == "__main__":
    # Run this file directly to create the database tables.
    print("Creating database tables...")
    with app.app_context():
        db.drop_all()
        db.create_all()

    print("Done!")
