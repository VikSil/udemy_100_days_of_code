import os
import pandas as pd


def main():

    # TODO 1. Create a dictionary in this format:
    {"A": "Alfa", "B": "Bravo"}

    current_dir = os.path.dirname(os.path.realpath(__file__))
    alphabet_df = pd.read_csv(f'{current_dir}/nato_phonetic_alphabet.csv')
    alphabet_dict = {row.letter: row.code for (index, row) in alphabet_df.iterrows()}

    # TODO 2. Create a list of the phonetic code words from a word that the user inputs.
    got_a_word = False
    while not got_a_word:
        user_word = input("Enter a word: ")
        user_letters = [letter for letter in user_word.upper()]
        try:
            user_phonetics = [alphabet_dict[key] for key in user_letters]
        except KeyError:
            print('Only latin alphabet letters are allowed')
        else:
            got_a_word = True

    print(user_phonetics)


if __name__ == "__main__":
    main()
