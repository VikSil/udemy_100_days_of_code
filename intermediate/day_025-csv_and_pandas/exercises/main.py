import os
import csv
import pandas


def main():

    # csv import with csv reader
    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(f'{current_dir}/weather_data.csv') as file:
        data = csv.reader(file)
        temperatures = [int(row[1]) for row in data if row[1] != 'temp']

    # csv import with pandas
    temperatures = pandas.read_csv(f'{current_dir}/weather_data.csv')
    print(temperatures['temp'])
    temperatures_dict  =temperatures.to_dict()
    print(temperatures_dict)
    temperatures_list = temperatures['temp'].to_list()
    print(temperatures_list)

    # data manipulation
    average_temperature = round(temperatures.temp.mean(),2)
    print(average_temperature)

    max_temperature = temperatures.temp.max()
    print(max_temperature)

    monday_weather = temperatures[temperatures.day == 'Monday']
    print(monday_weather)

    hottest_day = temperatures[temperatures.temp == temperatures.temp.max()]
    print(hottest_day)

    moday_temperature_F = monday_weather.temp[0] *  9/5 + 32
    print(moday_temperature_F)

    # creating dataframe
    data_dict = {
        'students': ['Amy', 'James', 'Angela'],
        'scores': [76, 56, 65]
    }
    data = pandas.DataFrame(data_dict)
    print(data)
    data.to_csv(f'{current_dir}/data_output.csv')

if __name__ == "__main__":
    main()
