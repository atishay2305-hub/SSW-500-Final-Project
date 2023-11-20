from . import db  # Assuming you've initialized PyMongo as `db`
from flask_login import UserMixin
from datetime import datetime

class Note:
    def create(self, data, user_id):
        current_time = datetime.utcnow()
        note = {
            "data": data,
            "date": current_time,
            "user_id": user_id
        }
        db.db.notes.insert_one(note)  # Accessing the 'notes' collection using db.db.notes
        return note

    def get_by_user_id(self, user_id):
        return db.db.notes.find({"user_id": user_id})  # Accessing the 'notes' collection using db.db.notes

class User(UserMixin):
    def create(self, email, password, first_name):
        user = {
            "email": email,
            "password": password,
            "first_name": first_name
        }
        db.db.users.insert_one(user)  # Accessing the 'users' collection using db.db.users
        return user

    def get_by_email(self, email):
        return db.db.users.find_one({"email": email})  # Accessing the 'users' collection using db.db.users
