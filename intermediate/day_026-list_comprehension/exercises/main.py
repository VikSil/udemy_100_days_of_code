import pandas
from random import randint


def main():
    names = ['Alex', 'Beth', 'caroline', 'Dave', 'Eleanor', 'Freddie']

    upercase_names = [name.upper() for name in names]
    print(upercase_names)

    student_scores = {student: randint(1, 100) for student in names}

    failed_students = {student: score for (student, score) in student_scores.items() if score < 60}

    print('Student scores are:')
    print(student_scores)
    print()
    print('Failed students are:')
    print(failed_students)
    print()

    student_dict = {'student': ['Angela', 'James', 'Lily'], 'score': [56, 76, 98]}

    student_df = pandas.DataFrame(student_dict)

    for index, row in student_df.iterrows():
        print(row)
        print(row.student)
        if row.student == 'Angela':
            print(row.score)

        print()


if __name__ == "__main__":
    main()
