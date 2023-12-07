from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import requests
import json
import secrets
import time
from requests.exceptions import RequestException

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['user_db']
users = db['users']

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.username

# Auth Blueprint
auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(username):
    user_data = users.find_one({'username': username})
    if user_data:
        return User(username=user_data['username'], password=user_data['password'])
    return None

def get_trivia_questions():
    API_URL = "https://opentdb.com/api.php"
    params = {"amount": 2, "category": 10}
    headers = {"User-Agent": "YourApp/1.0"}

    max_retries = 3
    current_retry = 0

    while current_retry < max_retries:
        try:
            url = f"{API_URL}?amount={params['amount']}&category={params['category']}"
            print(f"Request URL: {url}")
            print(f"Request Parameters: {params}")

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                questions_data = json.loads(response.text)
                questions_list = questions_data.get("results", [])
                return questions_list
            elif response.status_code == 429:
                print("Rate limit exceeded. Retrying after a delay...")
                time.sleep(5)  # Wait for 5 seconds before retrying
                current_retry += 1
            else:
                print(f"Error: {response.status_code}")
                return None

        except RequestException as e:
            print(f"RequestException: {e}")
            print("Retrying after a delay...")
            time.sleep(5)  # Wait for 5 seconds before retrying
            current_retry += 1

    print("Exceeded the maximum number of retries. Unable to fetch questions.")
    return None




@auth.route("/quiz")
@login_required
def quiz():
    questions_list = get_trivia_questions()
    print(questions_list)
    return render_template("quiz.html", questions_list=questions_list)

@auth.route("/submitquiz", methods=['POST', 'GET'])
@login_required
def submit():
    correct_count = 0
    questions_list = get_trivia_questions()

    if questions_list is None or not isinstance(questions_list, list):
        print("Error: Questions list is None or not iterable")
        return render_template("error.html"), 500

    for question in questions_list:
        question_id = str(question.get('id'))

        try:
            selected_option = request.form[question_id]
        except KeyError as e:
            print(f"KeyError: {e}")
            continue

        correct_option = question.get('correct_answer')

        print(f"Question ID: {question_id}")
        print(f"Selected Option: {selected_option}")
        print(f"Correct Option: {correct_option}")

        if selected_option == correct_option:
            correct_count += 1

    return render_template("result.html", correct_count=correct_count, total_questions=len(questions_list))

# Register the auth blueprint
app.register_blueprint(auth)

# Routes
@app.route('/')
def home():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return render_template('landing.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        existing_user = users.find_one({'username': username})
        if existing_user:
            flash('Username already exists!', category='error')
        else:
            new_user = {'username': username, 'password': hashed_password}
            users.insert_one(new_user)

            session['username'] = username
            flash('Registration successful!', category='success')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            login_user(User(username=user['username'], password=user['password']))
            return redirect(url_for('auth.quiz'))
        else:
            flash('Invalid username or password!', category='error')

    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('home'))

    return 'Method Not Allowed', 405

if __name__ == '__main__':
    app.run(debug=True)
