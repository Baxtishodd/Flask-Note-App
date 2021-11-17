from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    color = db.Column(db.String(100))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    avatar = db.Column(db.String(100), nullable=False, default='default.jpg')
    

    notes = db.relationship('Note')
    contacts = db.relationship('Contact')
    tasks = db.relationship('Task')


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    sname = db.Column(db.String(100))
    pnumber = db.Column(db.String(100))
    # avatar = db.Column(db.String(255))

    date = db.Column(db.DateTime(timezone=True), default=func.now())
    t_color = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) 
    task = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    due_date = db.Column(db.String(100))
    due_time = db.Column(db.String(100))
    status = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
