import os
import turtle
import pandas as pd


TOTAL_STATES = 50


def main():

    current_dir = os.path.dirname(os.path.realpath(__file__))
    image_path = current_dir + '/blank_states_img.gif'

    screen = turtle.Screen()
    screen.title("U.S. States Game")
    screen.addshape(image_path)

    turtle.shape(image_path)

    states = pd.read_csv(f'{current_dir}/50_states.csv')
    states_list = states.state.to_list()

    guessed_states = []
    while len(guessed_states) < TOTAL_STATES:
        prompt = screen.textinput(title=f'{len(guessed_states)}/{TOTAL_STATES} guessed', prompt='Type U.S. State Name')

        real_state = prompt.lower() in [state.lower() for state in states_list]
        newly_guessed = prompt.lower() not in [state.lower() for state in guessed_states]
        if real_state and newly_guessed:

            x_coord = states[states['state'].str.strip().str.match(prompt.lower(), case=False)]['x'].iloc[0]
            y_coord = states[states['state'].str.strip().str.match(prompt.lower(), case=False)]['y'].iloc[0]

            new_state = turtle.Turtle()
            new_state.up()
            new_state.hideturtle()
            new_state.goto(x_coord, y_coord)
            guessed_state = states[states['state'].str.strip().str.match(prompt.lower(), case=False)]['state'].iloc[0]
            guessed_states.append(guessed_state)
            new_state.write(guessed_state)

        if prompt == 'exit':
            break

    if len(guessed_states) == TOTAL_STATES:
        game_over = turtle.Turtle()
        game_over.up()
        game_over.hideturtle()
        game_over.color('green')
        game_over.write('WELL DONE', False, align='center', font=("Courier", 24, "normal"))

    else:
        states_to_learn = list(set(states_list).symmetric_difference(set(guessed_states)))
        states_to_learn.sort()
        states_to_learn_series = pd.Series(states_to_learn)
        states_to_learn_series.index += 1
        states_to_learn_series.to_csv(f'{current_dir}/states_to_learn.csv', header=False)


if __name__ == "__main__":
    main()
