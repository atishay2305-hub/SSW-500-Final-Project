# quiz_brain.py

class QuizBrain:
    def __init__(self):
        self.questions = []
        self.current_question_index = 0

    def add_question(self, question, correct_answer):
        self.questions.append({"question": question, "correct_answer": correct_answer})

    def get_next_question(self):
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            self.current_question_index += 1
            return question_data
        return None
