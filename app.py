from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required
import secrets
from models import Question

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

client = MongoClient('mongodb://localhost:27017/')
db = client['user_db']
users = db['users']

login_manager = LoginManager(app)
login_manager.login_view = 'login'

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
    questions = [
        Question(1, "What is the capital of France?", ["Paris", "Berlin", "London"], "Paris"),
        Question(2, "Which planet is known as the Red Planet?", ["Mars", "Venus", "Jupiter"], "Mars"),
        Question(3, "What is the largest mammal in the world?", ["Elephant", "Blue Whale", "Giraffe"], "Blue Whale"),
        Question(4, "In which year did World War II end?", ["1943", "1945", "1950"], "1945"),
        Question(5, "What is the chemical symbol for gold?", ["Au", "Ag", "Fe"], "Au"),
        Question(6, "Who wrote 'Romeo and Juliet'?", ["Charles Dickens", "William Shakespeare", "Jane Austen"], "William Shakespeare"),
        Question(7, "What is the largest ocean on Earth?", ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean"], "Pacific Ocean"),
        Question(8, "What is the speed of light?", ["299,792 kilometers per second", "150,000 kilometers per second", "450,000 kilometers per second"], "299,792 kilometers per second"),
        Question(9, "Who painted the Mona Lisa?", ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso"], "Leonardo da Vinci"),
        Question(10, "What is the capital of Japan?", ["Seoul", "Beijing", "Tokyo"], "Tokyo"),
    ]
    return questions


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
    questions_list = get_trivia_questions()
    return render_template("quiz.html", questions_list=questions_list)

@app.route('/submitquiz', methods=['POST', 'GET'])
@login_required
def submit():
    questions_list = get_trivia_questions()

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
