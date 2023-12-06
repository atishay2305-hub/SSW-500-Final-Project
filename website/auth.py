from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash  # Import generate_password_hash
from .models import User, Question
from . import db
from flask_login import login_user, login_required, current_user
import requests
import json

auth = Blueprint('auth', __name__)

def get_trivia_questions():
    API_URL = "https://opentdb.com/api.php"
    params = {"amount": 2, "category": 10}

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        questions_data = json.loads(response.text)
        # Extract the questions list from the data
        questions_list = questions_data.get("results", [])
        return questions_list
    else:
        print(f"Error: {response.status_code}")
        return None


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_collection = db.users
        user = user_collection.find_one({'email': email})
        # user_object=User()
        # user=user_object.get_by_email(email)
        if user:
            if check_password_hash(user['password'], password):
                flash('Logged in successfully!', category='success')
                #login_user(user, remember=True)
                return redirect(url_for('auth.quiz'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            users_collection = db.users  # Access MongoDB collection
            existing_user = users_collection.find_one({'email': email})

            if existing_user:
                flash('Email already exists.', category='error')
            else:
                hashed_password = generate_password_hash(password1, method='sha256')
                user_instance = User()

                # Call the create() method
                user_instance.create(email, hashed_password, first_name)

                flash('Account created!', category='success')
                login_user(User(user_instance.id, user_instance.email, user_instance.password, user_instance.first_name), remember=True)
                return redirect(url_for('auth.quiz'))

    return render_template("sign_up.html", user=current_user)

@login_required
@auth.route("/quiz")
def quiz():
    questions_list = get_trivia_questions()
    print(questions_list)
    return render_template("quiz.html", questions_list=questions_list)

@login_required
@auth.route("/submitquiz", methods=['POST', 'GET'])
def submit():
    correct_count = 0
    questions_list = get_trivia_questions()

    # Check if questions_list is None
    if questions_list is None:
        print("Error: Questions list is None")
        return render_template("error.html"), 500

    # Check if questions_list is iterable
    if not isinstance(questions_list, list):
        print("Error: Questions list is not iterable")
        return render_template("error.html"), 500

    for question in questions_list:
        # Modify this part based on the actual structure of the question data
        question_id = str(question.get('id'))  # Adjust based on the actual structure

        # Add debugging statements
        print(f"Question ID: {question_id}")
        print(f"Form data keys: {list(request.form.keys())}")

        try:
            selected_option = request.form[question_id]
        except KeyError as e:
            print(f"KeyError: {e}")
            continue  # Skip to the next iteration if the key is not present

        print(f"Selected option: {selected_option}")

        correct_option = question.get('correct_answer')  # Adjust based on the actual structure

        if selected_option == correct_option:
            correct_count += 1

    return render_template("result.html", correct_count=correct_count)



@auth.route('/', defaults={'path': ''})
@auth.route('/<path:path>')
def catch_all(path):
    return render_template("error.html"), 404
