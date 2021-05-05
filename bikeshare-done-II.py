import time
import pandas as pd
import numpy as np

CITY_DATA = { 'ch': 'chicago.csv',
              'ny': 'new_york_city.csv',
              'wa': 'washington.csv' }

days = {'Sat': 'Saturday', 'Sun': 'Sunday', 'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday', 'All': 'all'}

months = {"jan": 1, "feb": 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'all': 'all'}

def menu ():
    '''This function produces a menu to help the user choose which statistical analysis to view, 
       and to enable going back and forth between different options. The user is prompted to select
       their filters upon entering the application for the first time, then, they are given multiple
       options upon reaching the menu, which include resetting the filters to different settings.'''
    
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    city, month, day = get_filters()
    df = load_data(city, month, day)
    menus = True
    while menus:
        #The menu interface
        stats = input(
            '''\nWhat would you like to do?\n
            - Type "filter" to change your choice of city
            - Type "time" to view time statistics
            - Type "station" to view travel statistics
            - Type "trip" to view trip duration statistics
            - Type "user" to view user statistics
            - Type "raw" to view raw data
            - Type "q" to quit this application\n''').lower()
        
        # Reassign the data filters 
        if stats == 'filter':
            city, month, day = get_filters()
            df = load_data(city, month, day)
        
        #Display time statistics 
        elif stats == 'time':
            time_stats(df)
        
        #Display travel statistics 
        elif stats == 'station':
            station_stats(df)
        
        #Display trip duration statistics
        elif stats == 'trip':
            trip_duration_stats(df)
        
        #Display user statistics 
        elif stats == 'user':
            user_stats(df)
        
        #Display raw data
        elif stats == 'raw':
            raw_data(df)
        
        #Quit the application
        elif stats == 'q':
            print('\nSee you later!\n')
            menus = None
        else:
            print('\nThis input is invalid\n')
        


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    # Get user input for city (chicago, new york city, washington).
    city = input('\nPlease input the city: \n- ny for New york\n- ch for chicago\n- wa for washington \n').lower()
    
    # Validation step to check if the data entered is correct
    while city not in CITY_DATA.keys():
        print('\nThat is an invalid input\n')
        city = input('\nPlease input the city: \n- ny for New york\n- ch for chicago\n- wa for washington \n').lower()
    
    # Get user input for month (all, january, february, ... , june)
    month = input('\nPlease insert a month from Jan to Jun, or type \'all\' to display all months: \n').lower()
    
    # Validation step to check if the data entered is correct
    while month not in months.keys():
        print('\nThat is an invalid input \n')
        month = input('\nPlease insert a month from Jan to Jun, or type \'all\' to display all months: \n').lower()
    month = months [month]
   
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nPlease insert a day from Sun to Sat, or type \'all\' to display all days: \n').title()
    
    # Validation step to check if the data entered is correct
    while day not in days.keys():
        print('\nThat is an invalid input\n')
        day = input('\nPlease insert a day from Sun to Sat, or type \'all\' to display all days: \n').title()
    day = days [day]

    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # Extract month and day of week from Start Time to create new columns
    df['month'] = df ['Start Time'].dt.month
    df['day_of_week'] = df ['Start Time'].dt.weekday_name
    df['hour'] = df ['Start Time'].dt.hour
    
    
    # Add route column to help in the stations function
    df['Route'] = df['Start Station'] + ' - ' + df['End Station']
    
    # Add trip duration column to help in the trip duration function
    df['Trip Duration'] = df['End Time'] - df['Start Time']
    
    # Filter data by the month and day selected, provided the user did not select "all".
    if month != 'all':
        df = df [df ['month'] == month]
    if day != 'all':
        df = df [df ['day_of_week'] == day]
    return (df)

def time_stats (df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print('\nMost common month: ',df['month'].mode()[0])

    # Display the most common day of week
    print('Most common day of the week: ', df['day_of_week'].mode()[0])

    # Display the most common start hour
    print('Most common starting hour: {}:00'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n', '-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('Most commonly used start station is: {}'.format( df['Start Station'].value_counts().idxmax()))
    
    # Display most commonly used end station
    print('Most commonly used end station is: ', df['End Station'].value_counts().idxmax())
    
    
    # Display most frequent combination of start station and end station trip
    
    print('Most commonly used route: ', df['Route'].value_counts().idxmax() )
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('Total travel time: ', df['Trip Duration'].sum())

    # Display mean travel time
    print('Mean travel time: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of each user type: \n', df['User Type'].value_counts().to_frame())

    # Display counts of gender provided that Gender is supported in the data provided.
    
    if 'Gender' not in df.columns :
        print('\nGender data is not supported for this city')
    else:
        print('\nCount of each gender: \n', df['Gender'].value_counts().to_frame())

    # Display earliest, most recent, and most common year of birth, provided that Birth Year is supported in the data provided.
    if 'Birth Year' not in df.columns:
        print('\nBirth Year data is not supported for this city')
    else:
        print('\nEarliest birth year: ', int(df['Birth Year'].min()))
        print('\nMost recent birth year: ', int(df['Birth Year'].max()))
        print('\nMost common year of birth: ', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    
    

def raw_data (df):
    '''
    Ask the user if they want to display raw data. Data are displayed in increments of 5 rows 
    provided the user keeps choosing y to view more.
    '''
    
    x = 5
    print(df.head(x))
    answer = input('\nWould you like to display more? Type y or n\n').lower()
    while answer == 'y':
        x += 5
        print(df.head(x))
        answer = input('\nWould you like to display more? Type y or n\n').lower()
        
    
def main():
    menu()

if __name__ == "__main__":
	main()
