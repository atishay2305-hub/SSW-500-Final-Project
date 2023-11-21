from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from bson import ObjectId
from views import views
from quiz import quiz  # Import the quiz Blueprint

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/SSW-500"
mongo = PyMongo(app)

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(quiz, url_prefix="/quiz")  # Register the quiz Blueprint

def create_app():
    app = Flask(__name__)
    
    # Add your app configuration and routes here

    return app

app = create_app()

# Configure MongoDB
app.config['MONGO_URI'] = "mongodb://localhost:27017/SSW-500"
mongo = PyMongo(app)

# Register the 'views' blueprint
app.register_blueprint(views, url_prefix="/")

# Define the Question class
class Question:
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

# Create instances of the Question class
q1 = Question(1, "What is your University Name?", "Stevens", "NJIT", "ASU", 1)
q2 = Question(2, "Where UET is located", "Hoboken", "Jersey City", "New York", 3)
q3 = Question(3, "What is your degree name?", "SWE", "CS", "MIS", 2)

# Create a list of questions
questions_list = [q1, q2, q3]

# Define routes
@app.route("/quiz")
def quiz():
    return render_template("quiz.html", questions_list=questions_list)

@app.route("/submitquiz", methods=['POST', 'GET'])
def submit():
    correct_count = 0
    for question in questions_list:
        question_id = str(question.q_id)
        selected_option = request.form[question_id]
        correct_option = question.get_correct_option()
        if selected_option == correct_option:
            correct_count += 1

    return str(correct_count)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("error.html"), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8000)
