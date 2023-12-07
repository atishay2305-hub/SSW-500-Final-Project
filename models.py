# models.py
class Question:
    def __init__(self, q_id, question, options, correct_option):
        self.q_id = q_id
        self.question = question
        self.options = options
        self.correct_option = correct_option

    def to_dict(self):
        return {
            'q_id': self.q_id,
            'question': self.question,
            'options': self.options,
            'correct_option': self.correct_option
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            q_id=data['q_id'],
            question=data['question'],
            options=data['options'],
            correct_option=data['correct_option']
        )
