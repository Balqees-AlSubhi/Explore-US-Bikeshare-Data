import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def check_data_entry(prompt, valid_entries):
    try:
        user_input = str(input(prompt)).lower()
        while user_input not in valid_entries:
            print("\nIt looks like your entry is incorrect.\n")
            print("\nLet's try again!\n")
            user_input = str(input(prompt)).lower()

        print("\nGreat! You've chosen: {}\n".format(user_input))
        return user_input

    except:
        print("\nThere seems to be an issue with your input.\n")

def get_filters():
    print("\nHello! Let's explore some US bikeshare data!\n")
    valid_cities = CITY_DATA.keys()
    prompt_cities = 'Choose one of the 3 cities (Chicago, New York City, Washington): '
    city = check_data_entry(prompt_cities, valid_cities)

    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    prompt_month = 'Choose a month (all, january, february, ... , june): '
    month = check_data_entry(prompt_month, valid_months)

    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    prompt_day = 'Choose a day (all, monday, tuesday, ... sunday): '
    day = check_data_entry(prompt_day, valid_days)

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    print('\nCalculating The Most Popular Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', popular_start_station)

    popular_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', popular_end_station)

    df['Route'] = df['Start Station'] + ' to ' + df['End Station']
    popular_route = df['Route'].mode()[0]
    print('Most Common Route:', popular_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    start_idx = 0
    end_idx = 5
    while True:
        show_raw_data = input("\nWould you like to see 5 lines of raw data? Enter 'yes' or 'no': ").lower()
        if show_raw_data != 'yes':
            break
        print(df.iloc[start_idx:end_idx])
        start_idx += 5
        end_idx += 5
        if start_idx >= len(df):
            print("\nNo more raw data to display.")
            break

def main():
    pd.set_option("display.max_columns", 200)
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        print("\nGenerating statistics based on the filtered data...\n")
        print("Total trips:", len(df))
        print("Most common start station:", df['Start Station'].mode()[0])
        print("Most common end station:", df['End Station'].mode()[0])
        print("Total travel time (seconds):", df['Trip Duration'].sum())
        print("Mean travel time (seconds):", df['Trip Duration'].mean())
        print("Counts of each user type:\n", df['User Type'].value_counts())

        if 'Gender' in df:
            print("Counts of each gender:\n", df['Gender'].value_counts())

        if 'Birth Year' in df:
            print("Earliest birth year:", int(df['Birth Year'].min()))
            print("Most recent birth year:", int(df['Birth Year'].max()))
            print("Most common birth year:", int(df['Birth Year'].mode()[0]))

        time_stats(df)
        station_stats(df)
        display_raw_data(df)

        restart = input("\nWould you like to restart? Enter 'yes' or 'no': ")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
