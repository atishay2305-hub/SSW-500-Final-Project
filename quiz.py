#Created quiz file for Questions and answers

from flask import Blueprint, render_template, request, jsonify
from app import Question

quiz = Blueprint("quiz", __name__)

@quiz.route("/quiz")
def show_quiz():
    # You can add logic here to fetch questions from the database if needed
    # For now, we will use the predefined list of questions from app.py
    questions_list = app.questions_list
    return render_template("quiz.html", questions_list=questions_list)

@quiz.route("/submitquiz", methods=['POST'])
def submit_quiz():
    try:
        questions_list = app.questions_list
        correct_count = 0
        for question in questions_list:
            question_id = str(question.q_id)
            selected_option = request.form.get(question_id)
            correct_option = question.get_correct_option()
            if selected_option == correct_option:
                correct_count += 1

        return jsonify({"correct_count": correct_count, "total_questions": len(questions_list)})
    
    except Exception as e:
        return jsonify({"error": str(e)})

