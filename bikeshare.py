import time
import pandas as pd
import numpy as np

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city: str = input(
        'Please enter name of one city from the next \'chicago\' or \'new york city\' or \'washington\': ').lower()
    while city not in CITY_DATA.keys():
        print("please enter valid city name")
        city: str = input(
            'Please enter name of one city from the next \'chicago\' or \'new york city\' or \'washington\': ').lower()
    # get user input for month (all, january, february, ... , june)
    month: str = input(
        'Please enter name of one month from the next \'january\' or \'february\' or \'march\' or \'april\' '
        'or \'may\' or \'june\' or you can choose \'all\': ').lower()
    if month != 'all':
        while (month not in months):
            print("please enter valid month name")
            month: str = input(
                'Please enter name of one month from the next \'january\' or \'february\' or \'march\' or \'april\' '
                'or \'may\' or \'june\' or you can choose \'all\': ').lower()
    else:
        month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day: str = input(
        'Please enter name of one day from the next \'Monday\' or \'Tuesday\' or \'Wednesday\' or \'Thursday\' '
        'or \'Friday\' or \'Saturday\' or \'Sunday\' or simply can choose \'All\': ').title()
    if day != 'all':
        while (day not in days):
            print("please enter valid day name")
            day: str = input(
                'Please enter name of one day from the next \'Monday\' or \'Tuesday\' or \'Wednesday\' or \'Thursday\' '
                'or \'Friday\' or \'Saturday\' or \'Sunday\' or simply can choose \'All\': ').title()
    else:
        day = 'all'

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA.get(city))

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # filter start month from Start Time and create month column
    df['Start month'] = df['Start Time'].dt.month
    df['Start day'] = df['Start Time'].dt.day_name()
    df['Start hour'] = df['Start Time'].dt.hour

    # filter by month
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['Start month'] == month]
    # filter by day
    if day != 'All':
        df = df[df['Start day'] == day.title()]

    print("Done")

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        popular_month = df["Start month"].dropna()
        if popular_month.empty:
            print("No popular month found, please try again with different month")
        else:
            month = df['Start month'].mode()[0]
            print(f"The Most common month is {months[month - 1]}")
    else:
        print("Select all to get the most popular month")

        # display the most common day of week'
    if day == 'All':
        popular_day = df["Start day"].dropna()
        if popular_day.empty:
            print("No popular day found, please try again with different month")
        else:
            day = df['Start day'].mode()[0]
            print(f"The Most common day is {day}")
    else:
        print("Select all to get the most popular day")

    # display the most common start hour
    most_common_houre = df['Start hour'].mode()[0]
    print(f"The Most common hour of the week is: {most_common_houre}:00 hrs")

    print(f"\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print(f"The Most common used start station is {start_station}")
    # display most commonly used end station
    End_station = df['End Station'].mode()[0]
    print(f"The Most common used End station is {End_station}")

    # display most frequent combination of start station and end station trip
    common_combination = df[['Start Station', 'End Station']]
    common_trip = (common_combination.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False))
    print(f"The Most common trip is {common_trip.index[0]}"
          )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_time = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).sum()
    print(f"Total trip duration is {total_trip_time} hrs")

    # display mean travel time
    mean_trip_time = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).mean()
    print(f"Average trip duration is {mean_trip_time} hrs")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print(f"Counts of user types is: \n {user_counts}")

    # Display counts of gender
    if "Gender" in df:
        count_gender = df["Gender"].dropna()
        if count_gender.empty is False:
            counts_of_gender = df['Gender'].value_counts()
            print(f"Counts of gender is :\n {counts_of_gender}")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        birth_y = df["Birth Year"].dropna()
        if birth_y.empty is False:
            earliest = df['Birth Year'].min()
            print(f"the Earliest Birthday is: {earliest}")
            most_recent = df['Birth Year'].max()
            print(f"The most recent Birthday is: {most_recent}")
            most_common = df['Birth Year'].mode()[0]
            print(f"The most common Birthday is: {most_common}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

#Show more function to show 5 rows each time user choose yes
def show_more(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue? Enter yes or no:").lower()



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_more(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
