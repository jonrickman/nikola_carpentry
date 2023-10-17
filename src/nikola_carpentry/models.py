import json
from nikola_carpentry import db, login_manager, app
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Column, String, Integer, Boolean, ForeignKey
from werkzeug.security import generate_password_hash


@login_manager.user_loader
def load_user(user_id: int):
    return AdminUser.query.get(int(user_id))


class AdminUser(db.Model, UserMixin):
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, username, password, email) -> None:
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()


class Project(db.Model):
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    posted = Column(DateTime(timezone=True), server_default=func.now())
    approved = Column(Boolean, default=False)
    files = db.relationship(
        "ProjectFile", secondary="project_x_file", back_populates="projects"
    )

    def __init__(self, title, content) -> None:
        self.title = title
        self.content = content

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def pretty_date(self) -> str:
        month = self.posted.strftime("%B")
        year = self.posted.strftime("%Y")
        return f"{month} {year}"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_files(self):
        return self.files


class ProjectFile(db.Model):
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    filepath = Column(String, nullable=False)
    projects = db.relationship(
        "Project", secondary="project_x_file", back_populates="files"
    )

    def __init__(self, filepath) -> None:
        self.filepath = filepath

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return self.filepath


class Contact(db.Model):
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    content = Column(String, nullable=True)
    sent = Column(Boolean, default=False)

    def __init__(self, contact_name, subject, email, phone, content) -> None:
        self.contact_name = contact_name
        self.subject = subject
        self.email = email
        self.phone = phone
        self.content = content


class Review(db.Model):
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    author = Column(String, nullable=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    posted = Column(DateTime(timezone=True), server_default=func.now())
    approved = Column(Boolean, nullable=False, default=False)

    def __init__(self, rating, author, title, content) -> None:
        self.rating = rating
        self.author = author
        self.title = title
        self.content = content

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def pretty_date(self) -> str:
        month = self.posted.strftime("%B")
        year = self.posted.strftime("%Y")
        return f"{month} {year}"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


project_x_file = db.Table(
    "project_x_file",
    Column("project_file_id", Integer, ForeignKey("project_file.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
    extend_existing=True,
)


if __name__ == "__main__":
    # Run this file directly to create the database tables.
    print("Creating database tables...")
    with app.app_context():
        db.drop_all()
        db.create_all()

    print("Done!")
