from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    tel = db.Column(db.String(1000))
    stat = db.Column(db.Boolean, default=False)
    employee = db.Column(db.Boolean, default=False)
    depart = db.Column(db.String(1000))

class Depart(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(100))