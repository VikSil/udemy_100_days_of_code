import os
import pandas as pd


def main():

    current_dir = os.path.dirname(os.path.realpath(__file__))
    squirrels = pd.read_csv(f'{current_dir}/2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv')
    black_ones = squirrels[squirrels['Primary Fur Color'] == 'Black']
    red_ones = squirrels[squirrels['Primary Fur Color'] == 'Cinnamon']
    gray_ones = squirrels[squirrels['Primary Fur Color'] == 'Gray']

    summary = {
        'grey': gray_ones.shape[0],
        'red': red_ones.shape[0],
        'black': black_ones.shape[0],
    }

    sumary_df = pd.DataFrame(list(summary.items()), columns=['Fur Color', 'Count'])
    sumary_df.to_csv(f'{current_dir}/squirrel_count.csv')


if __name__ == "__main__":
    main()
