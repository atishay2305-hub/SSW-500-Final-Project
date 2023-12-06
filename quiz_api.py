import requests

def get_trivia_question():
    url = "https://opentdb.com/api.php?amount=48"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        question = data.get("question")
        answers = data.get("answers", [])
        return question, answers
    else:
        print(f"Error: {response.status_code}")
        return None, None

if __name__ == "__main__":
    question, answers = get_trivia_question()

    if question is not None:
        print("Question:", question)
        print("Answers:", answers)
