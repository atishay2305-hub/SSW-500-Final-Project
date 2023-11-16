# quiz_server.py
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/quiz_db"  # Change the URI accordingly
mongo = PyMongo(app)

from quiz_brain import QuizBrain

quiz_brain = QuizBrain()

# Add some sample questions
quiz_brain.add_question("What is the capital of France?", "Paris")
quiz_brain.add_question("What is 2 + 2?", "4")
# Add more questions as needed

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        question_data = quiz_brain.get_next_question()
        if question_data:
            return jsonify(question_data)
        else:
            return jsonify({"message": "Quiz completed!"})

    elif request.method == 'POST':
        data = request.json
        user_data = {
            "name": data["name"],
            "marks": data["marks"],
            "quiz_attempted": data["quiz_attempted"]
        }
        mongo.db.users.insert_one(user_data)
        return jsonify({"message": "User data stored successfully!"})


if __name__ == '__main__':
    app.run(debug=True)
