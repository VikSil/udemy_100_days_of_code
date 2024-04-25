from question_model import *
from quiz_brain import *
from data import *


def main():

    question_bank = []
    for q in question_data:
        question_bank.append(Question(txt = q['text'], answer = q['answer']))

    quiz = QuizBrain(question_bank)
    while quiz.still_has_questions():
        quiz.next_question()
    
    print('You have completed the quiz')
    print(f'Your final score was: {quiz.score}/{len(question_bank)}')

if __name__ == "__main__":
    main()
