from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # e.g., 'officer'

    def __repr__(self):
        return f'<User {self.username}>'

class Prisoner(db.Model):
    __tablename__ = 'prisoners'
    id = db.Column(db.Integer, primary_key=True)
    prisoner_id = db.Column(db.String(20), unique=True, nullable=False)  # e.g., '2024-001'
    name = db.Column(db.String(64), nullable=False)
    crime = db.Column(db.String(128), nullable=False)
    block = db.Column(db.String(20), nullable=False)
    date_in = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='在押')  # '在押' or '已释放'
    date_out = db.Column(db.DateTime)
    release_type = db.Column(db.String(20))

    def __repr__(self):
        return f'<Prisoner {self.prisoner_id}: {self.name}>'