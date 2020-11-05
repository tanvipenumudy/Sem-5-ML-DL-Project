from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    cname = db.Column(db.String(1000))
    dob = db.Column(db.String(10))
    school = db.Column(db.String(1000))
    clas = db.Column(db.String(100))
    gender = db.Column(db.String(6))
    lang = db.Column(db.String(100))
    mother = db.Column(db.String(1000))
    father = db.Column(db.String(1000))
    phone = db.Column(db.Integer)
    location = db.Column(db.String(5000))
    concern = db.Column(db.String(10000))
    schonell = db.Column(db.Integer)
    wepman = db.Column(db.Integer)
    burt = db.Column(db.Integer)
    sch = db.Column(db.String(10))
    sch1 = db.Column(db.Integer)
    bur = db.Column(db.String(10))
    bur1 = db.Column(db.Integer)
    wep = db.Column(db.String(10))
