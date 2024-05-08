import requests
from pathlib import Path
from question_model import Question
from quiz_brain import QuizBrain
from ui import QuizInterface

BASE_DIR = Path(__file__).resolve().parent


def main():
    question_data = refresh_questions()
    question_bank = []
    for question in question_data:
        question_text = question["question"]
        question_answer = question["correct_answer"]
        new_question = Question(question_text, question_answer)
        question_bank.append(new_question)

    quiz = QuizBrain(question_bank)
    quiz_ui = QuizInterface(quiz)


def refresh_questions():
    parameters = {'amount': 10, 'type': 'boolean', 'category': 18}
    response = requests.get('https://opentdb.com/api.php', params=parameters)
    response.raise_for_status()
    data = response.json()
    return data['results']


if __name__ == "__main__":
    main()
