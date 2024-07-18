from flask_sqlalchemy import SQLAlchemy
from . import db
class User(db.Model):
    id=db.Column(db.String(15),primary_key=True)
    password=db.Column(db.String(100))
    
class es_data(db.Model):
    id=db.Column(db.String(15),primary_key=True)
    filename=db.Column(db.String(50))
    tokens=db.Column(db.Integer)
    session_time=db.Column(db.Integer)
    file_size=db.Column(db.Integer)