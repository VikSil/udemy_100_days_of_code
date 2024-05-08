class QuizBrain:

    def __init__(self, q_list):
        self.question_number = 0
        self.question_list = q_list
        self.score = 0

    def next_question(self):
        question = self.question_list[self.question_number]
        self.question_number += 1
        response = input(f'Q.{self.question_number}: {question.txt} (True/False)?: ')
        self.check_answer(response, question.answer)

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def check_answer(self, response, correct_answer):
        if response.lower() == correct_answer.lower():
            print("You're right!")
            self.score += 1
        else:
            print("That's wrong.")
        print(f"Your current score is: {self.score}/{self.question_number}")
        print()
