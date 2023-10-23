
correct_answers_counter = 0

with open("questionDump.py", 'r') as file:
    content = file.read()

def getCorrectAnswers():
    try:
        data_dict = eval(content)
        print(data_dict)
        if data_dict == "questions":
            questions = data_dict
            for question in questions:
                print("Options: ")
                for i in range(len(question["incorrect_answers"])):
                    print(f"{i+1}. {question['incorrect_answers'][i]}")
                print(f"{len(question['incorrect_answers'])+1}. {question['corrrect_answer']}")
                user_answer = int(input("Enter the number of your answer: "))
                if user_answer == len(question["incorrect_answers"]) + 1:
                    print("Correct!")
                    correct_answers_counter += 1
                else:
                    print("Incorrect.")    
        response = (f"You got {correct_answers_counter} out of {len(questions)} questions correct.")
        return response

    except SyntaxError:
        response = "Error: There was a syntax error in the file. Make sure it's a valid Python dictionary."
        return response

    