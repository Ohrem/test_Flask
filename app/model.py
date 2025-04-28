from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)


class ToastMessage(db.Model):
    __tablename__ = 'toast_messages'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime)
    user = db.relationship('User', backref='toast_messages')