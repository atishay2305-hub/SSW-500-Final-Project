from . import db  # Assuming you've initialized PyMongo as `db`
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin):
    def create(self, email, password, first_name):
        user = {
            "email": email,
            "password": password,
            "first_name": first_name
        }
        db.users.insert_one(user)  # Accessing the 'users' collection using db.db.users
        return user

    def get_by_email(self, email):
        return db.users.find_one({"email": email})  # Accessing the 'users' collection using db.db.users

class Question():
    def __init__(self, q_id, question, option1, option2, option3, correctOption):
        self.q_id = q_id
        self.question = question
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.correctOption = correctOption

    def get_correct_option(self):
        if self.correctOption == 1:
            return self.option1
        elif self.correctOption == 2:
            return self.option2
        elif self.correctOption == 3:
            return self.option3
 