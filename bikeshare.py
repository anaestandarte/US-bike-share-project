import time
from datetime import timedelta
import pandas as pd
import numpy as np

city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyse.

    Returns:
        (str) city - name of the city to analyse
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington)
    city = input('Would you like to see the data for Chicago, New York City or Washington? ').lower()
    print('')
    while city not in ['chicago', 'new york city', 'washington']:
        city = input('Please select only from the given cities: ').lower()
        print('')

    # filter data by month, day of week, both, or not at all
    filter = input('Would you like to filter the data by month, day, both, or not at all?\nType no if no filtering is required. ').lower()
    print('')
    while filter not in ['month', 'day', 'both', 'no']:
        filter = input('Please select from month, day, both, or no: ').lower()
        print('')

    # set day and month initially to all for no filtering
    day = 'all'
    month = 'all'

    # get user input for month if filtering by both or month (january, february..)
    if filter in ['both', 'month']:
        month = input('Which month? January, February, March, April, May, or June? ').lower()
        print('')
        while month not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('Please select only from the given months: ').lower()
            print('')

    # get user input for day if filtering by both or day (monday, tuesday...)
    if filter in ['both', 'day']:
        day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ').lower()
        print('')
        while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            day = input('Please select only from the given days of the week: ').lower()
            print('')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyse
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(city_data[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    return df

def find_maxmin(df, var, d, s=None):
    """
    Finds the indices of the maximum and minimum values in a given dataframe column and prints the results

    Args:
        (Pandas dataframe) df - dataframe column to analyse
        (str) var - name of the variable being analysed (eg. month, hour, birthyear)
        (str) d - delimiter used in separating more than one index on output
        (str) s - additional formatting for output; optional argument
    """

    #finds the indices of the maximum and minimum values
    #idxmax() and idxmin() not used in case there are more than one max and min
    counts = df.value_counts()
    counts_max = counts.index[counts.iloc[:]==counts.max()].tolist()
    counts_min = counts.index[counts.iloc[:]==counts.min()].tolist()

    #changing month name from 1-6 to January-June
    if s == 'month':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        counts_max_name = [months[m-1] for m in counts_max]
        counts_min_name = [months[m-1] for m in counts_min]
        counts_max = counts_max_name
        counts_min = counts_min_name

    #converts integer into string for output (Note: join is used in printing the results, hence string is necessary)
    if s == 'inttostr':
        counts_max_str = [str(int(i)) for i in counts_max]
        counts_min_str = [str(int(i)) for i in counts_min]
        counts_max = counts_max_str
        counts_min = counts_min_str

    #Prints the index of the maximum and minimum values and the corresponding counts
    print('Most common {}: {}  Counts: {}'.format(var, d.join(counts_max), counts.max()))
    print('Least common {}: {}  Counts: {}'.format(var, d.join(counts_min), counts.min()))

def time_stats(df, month, day):
    """Displays statistics on the most and least frequent times of travel."""

    print('\nCalculating The Most and Least Frequent Times of Travel...')
    print('Filter: Month = {} and Day = {}\n'.format(month.title(), day.title()))

    start_time = time.time()

    # display the most and least common month
    if month == 'all':
        find_maxmin(df['Month'], 'month', ', ', 'month')
        print('')

    # display the most and least common day of week
    if day == 'all':
        find_maxmin(df['Day of Week'], 'day of week', ', ')
        print('')

    # display the most and least common start hour
    df['Hour'] = df['Start Time'].dt.hour
    find_maxmin(df['Hour'], 'hour', ', ', 'inttostr')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most and Least Popular Stations and Trip...')
    print('Filter: Month = {} and Day = {}\n'.format(month.title(), day.title()))

    start_time = time.time()

    # display most and least commonly used start station
    find_maxmin(df['Start Station'], 'start station', '\n')
    print('')

    # display most and least commonly used end station
    find_maxmin(df['End Station'], 'end station', '\n')
    print('')

    # display most frequent combination of start station and end station trip
    counts_trip = df.groupby(['Start Station', 'End Station']).size()
    trip_max = counts_trip.index[counts_trip.iloc[:]==counts_trip.max()].tolist()
    trip_max_out = ''
    for trip in trip_max:
        trip_max_out += '{} to {}\n'.format(*trip)
    print('Most common trip: {}  Counts: {}'.format(trip_max_out.strip(), counts_trip.max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    print('Filter: Month = {} and Day = {}\n'.format(month.title(), day.title()))

    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time: {}'.format(timedelta(seconds=float(total_time))))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Average travel time: {}'.format(timedelta(seconds=float(mean_time))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, month, day, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    print('Filter: Month = {} and Day = {}\n'.format(month.title(), day.title()))

    start_time = time.time()

    # Display counts of user types
    counts_user = df['User Type'].value_counts()
    counts_user_out=''
    for i, v in zip(counts_user.index.tolist(), counts_user.values.tolist()):
        counts_user_out += '{}: {}  '.format(i,v)
    print('User Type\n{}'.format(counts_user_out))

    if city != 'washington':
        # Display counts of gender
        gender = df['Gender'].value_counts()
        gender_out=''
        for i, v in zip(gender.index.tolist(), gender.values.tolist()):
            gender_out += '{}: {}  '.format(i,v)
        print('\nGender\n{}\n'.format(gender_out))

        # Display earliest, most recent, and most common year of birth
        birthyear_earliest = int(df['Birth Year'].min())
        birthyear_recent = int(df['Birth Year'].max())
        print('Birth Year\nEarliest birth year: {}\nMost recent birth year: {}'.format(birthyear_earliest, birthyear_recent))
        find_maxmin(df['Birth Year'], 'birth year', ', ', 'inttostr')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df, month, day)
        trip_duration_stats(df, month, day)
        user_stats(df, month, day, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
