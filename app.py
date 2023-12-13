from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required
import secrets
from models import Question
import requests
import html
import random

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

client = MongoClient('mongodb://localhost:27017/')
db = client['user_db']
users = db['users']

login_manager = LoginManager(app)
login_manager.login_view = 'login'

questions_list=[]

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    user_data = users.find_one({'username': username})
    if user_data:
        return User(username=user_data['username'], password=user_data['password'])
    return None

def get_trivia_questions():

    url = "https://opentdb.com/api.php?amount=5"

    response = requests.get(url)

    q=[]
    inc_ans=[]
    cor_ans=[]

    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            questions = data['results']
            for question in questions:
                decoded_question = html.unescape(question.get('question'))  # Decode HTML entities
                print("Question:", decoded_question)
                q.append(decoded_question)
                print("Correct Answer:", question.get('correct_answer'))
                cor_ans.append(question.get('correct_answer'))
                print("Incorrect Answers:", question.get('incorrect_answers'))
                inc_ans.append(question.get('incorrect_answers'))
                print("Category:", question.get('category'))
                print("Difficulty:", question.get('difficulty'))
                print("------------------------")
        else:
            print("No 'results' found in the response.")    
    else:
        print(f"Error: {response.status_code}")

    for i in range(5):
        random_index = random.randint(0, len(inc_ans[i])+1)  # Generate a random index
        inc_ans[i].insert(random_index, cor_ans[i])


    quiz_questions = [
        Question(1, q[0], inc_ans[0], cor_ans[0]),
        Question(2, q[1], inc_ans[1], cor_ans[1]),
        Question(3, q[2], inc_ans[2], cor_ans[2]),
        Question(4, q[3], inc_ans[3], cor_ans[3]),
        Question(5, q[4], inc_ans[4], cor_ans[4]),
    ]

    return quiz_questions


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

            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            login_user(User(username=user['username'], password=user['password']))
            return redirect(url_for('dashboard'))
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

@app.route('/quiz')
@login_required
def quiz():
    global questions_list
    questions_list = get_trivia_questions()
    return render_template("quiz.html", questions_list=questions_list)

@app.route('/submitquiz', methods=['POST', 'GET'])
@login_required
def submit():
    global questions_list

    if questions_list is None or not isinstance(questions_list, list):
        print("Error: Questions list is None or not iterable")
        return render_template("error.html"), 500

    correct_count = 0
    feedback_list = []

    for index, question in enumerate(questions_list):
        question_id = str(question.q_id)


        try:
            selected_option = request.form[question_id]
        except KeyError as e:
            print(f"KeyError: {e}")
            continue

        correct_option = str(question.correct_option)

        print(f"Question ID: {question_id}")
        print(f"Selected Option: {selected_option}")
        print(f"Correct Option: {correct_option}")

        if str(selected_option) == correct_option:
            correct_count += 1

        feedback_list.append({
            'index': index,
            'selected_option': selected_option,
            'correct_option': correct_option,
            'is_correct': str(selected_option) == correct_option
        })

    return render_template("result.html", correct_count=correct_count, total_questions=len(questions_list), feedback_list=feedback_list)

if __name__ == '__main__':
    app.run(debug=True)
