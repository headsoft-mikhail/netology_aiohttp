from app import db
from sqlalchemy import sql
from config import SALT
import hashlib


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(128), index=True)
    name = db.Column(db.String(50))

    def __str__(self):
        return f'User {self.email} ({self.name})'

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    def hash_password(self, raw_password):
        raw_password = f'{raw_password}{SALT}'
        self.password = hashlib.md5(raw_password.encode()).hexdigest()

    def verify_password(self, raw_password):
        raw_password = f'{raw_password}{SALT}'
        return self.password == hashlib.md5(raw_password.encode()).hexdigest()


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), index=True)
    text = db.Column(db.String(1000), index=True)
    created_at = db.Column(db.DateTime, server_default=sql.func.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __str__(self):
        return f'Post {self.title} ({self.created_at})'

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'owner_id': self.owner_id
        }
