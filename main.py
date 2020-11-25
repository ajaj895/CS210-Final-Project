# Link to assignment: https://westernonline.wiu.edu/d2l/le/content/169197/viewContent/2469388/View?ou=169197
# Data used: https://www.kaggle.com/vinaypratap/flight-price

# Authors: Evan Colwell
#          Gavin Horner
# Date: November 2020
# School: Western Illinois University
# Class: CS210: Python for Data Exploration

import pandas as pd

flights_df = pd.read_csv("Data_Train.csv")  # Open our data file and store it as a data frame for use within the methods
unique_airlines = set(flights_df.Airline)  # A set of unique airlines declared early for use in option 9.
unique_airlines_list = list(
    unique_airlines)  # A list of unique airlines for easy index access declared early for use in option 7
num_of_flights = len(flights_df.Airline)  # Length of the dataset for use in any option 1 and 7

pd.set_option('display.width', 320)
pd.set_option("display.max_columns", 11)  # All necessary for proper formatting in the Run output box
pd.set_option("display.max_rows", 10683)  # Comment out as needed


# Option 1 (Gavin) COMPLETED
# search_by_source_destination() searches flights by the user's given source, destination, day, and month
# and returns a dataframe with any flights matching the user's input. If there is no matches, the user will
# be informed of this.
def search_by_source_destination():
    print("You chose option 1.")
    source = input("Please enter a source: ")
    destination = input("Please enter a destination: ")
    day = input("Please enter a day: ")
    month = input("Please enter a month: ")

    date = f'{day}/{month}/2019' # Declare our date, 2019 static as all entries are from 2019
    user_source = flights_df.Source == source  # Condition so the sources match
    user_destination = flights_df.Destination == destination # Condition so the destinations match
    user_date = flights_df.Date_of_Journey == date # Condition so the dates match

    user_flights = flights_df[user_source & user_destination & user_date]  # Assign any matching flights to user_flights

    if user_flights.size > 0:  # If there are any matching flights
        print(user_flights) # Print any flights matching the conditions
    else:
        print("Sorry, there were no flights matching the data you entered. Please try again.")


# Option 2 (Evan) - Completed
# search_by_source_departure_by_date() searches for flights based on starting city and date range
# Handles errors from the user and will not continue until the user enters the correct input
def search_by_source_departure_by_date():
    print("You chose option 2.")
    print('____________________________________')
    start_city = input('Enter the starting city: ').capitalize()  # Makes sure that the format is not a problem

    # --- Error Handling with input ---
    while 1:
        error = False
        start_range = input('Enter the first day in your range (month/day): ')
        end_range = input('Enter the last day in your range (month/day): ')
        temp_start_list = start_range.split('/')
        temp_end_list = end_range.split('/')

        try:  # Checks for if a non int has been entered
            int(temp_start_list[0])
            int(temp_start_list[1])
            int(temp_end_list[0])
            int(temp_end_list[1])
        except ValueError:  # When the string can't be turned into an int
            print('____________________________________')
            print('Error! A date with numbers must be used (ex. 1/10, 5/18).')
            print('____________________________________')
            continue  # Returns to the top of the while loop
        # If the months are the same but the end date is before the start date, compares ascii codes not int values
        if temp_start_list[0] == temp_end_list[0] and int(temp_start_list[1]) > int(temp_end_list[1]):
            error = True
            print('____________________________________')
            print('Error! End date can not be before start date.')
            print('____________________________________')
        # End month before start month. This only works since our dataset is one year, doesn't work for Dec-Jan flights
        elif temp_start_list[0] > temp_end_list[0]:
            error = True
            print('____________________________________')
            print('Error! End date can not be before start date.')
            print('____________________________________')
        if not error:  # If no error has occurred
            break
    # --- End of error handling ---

    date_range = []  # List of dates, each element is list of a date ['day', 'month', 'year']

    if temp_start_list[0] == temp_end_list[0]:  # Same month
        if int(temp_start_list[0]) < 10:  # Formats the month if less than 10 (ex 05, or 01)
            month = f'0{temp_start_list[0]}'
        else:
            month = temp_start_list[0]
        for i in range(int(temp_start_list[1]), int(temp_end_list[1])+1): # Inclusive
            day = f'{i}'
            if i < 10:  # Formats the day
                day = f'0{i}'
            str_date = [day, month, '2019']  # day month year, the / is not needed to store
            date_range.append(str_date)
    else:
        for m in range(int(temp_start_list[0]), int(temp_end_list[0])+1): # For each month inclusive
            if int(temp_start_list[0]) < 10:  # Formats the month if less than 10 (ex 05, or 01)
                month = f'0{m}'
            else:
                month = f'{m}'
            if m == int(temp_start_list[0]):  # The start month
                for d in range(int(temp_start_list[1]), 32):
                    day = f'{d}'
                    if d < 10:  # Formats the day
                        day = f'0{d}'
                    str_date = [day, month, '2019']  # day month year, the / is not needed to store
                    date_range.append(str_date)
            elif m == int(temp_end_list[0]):  # If the end month has been reached, inclusive
                for d in range(1, int(temp_end_list[1])+1):
                    day = f'{d}'
                    if d < 10:  # Formats the day
                        day = f'0{d}'
                    str_date = [day, month, '2019']  # day month year, the / is not needed to store
                    date_range.append(str_date)
            else:  # Any month in-between start and end month
                for d in range(1,32):
                    day = f'{d}'
                    if d < 10:  # Formats the day
                        day = f'0{d}'
                    str_date = [day, month, '2019']  # day month year, the / is not needed to store
                    date_range.append(str_date)
    hit = False # Used for telling if flights were found or not
    for i in range(0, num_of_flights):
        if flights_df.Source[i] == start_city:
            # If the city is located, then check for the date match
            check_date = flights_df.Date_of_Journey[i].split('/')
            for date in date_range:  # For each date in the list is better than each flight in the DB
                if check_date[1] == date[1]:  # Check month
                    if check_date[0] == date[0]:  # Check day
                        print('______________________________________________')  # For looks
                        print(flights_df.loc[i])
                        print('______________________________________________')  # For looks
                        hit = True
    if not hit:
        print('____________________________________')
        print('No flights found!')
        print('____________________________________')



# Option 3 (Gavin) COMPLETED
# find_cheapest() finds the cheapest flights from the user's given source and destination.
# This function will return a dataframe with any flights matching the user's input. If there is no matches,
# the user will be informed of this.
def find_cheapest():
    print("You chose option 3.")
    source = input("Please enter a source: ")
    destination = input("Please enter a destination: ")
    cheapest = 1000000000  # Assign an arbitrary number to be redefined
    for i in range(0, num_of_flights):  # For all flights in the dataset
        if flights_df.Source[i] == source:  # If the sources match
            if flights_df.Destination[i] == destination: # And the destinations match
                if flights_df.Price[i] < cheapest: # And the price is lower than the current cheapest
                    cheapest = flights_df.Price[i]  # Reassign cheapest to be that price

    user_source = flights_df.Source == source  # Condition so that the sources match
    user_destination = flights_df.Destination == destination  # Condition so that the destinations match
    cheapest_flight = flights_df.Price == cheapest  # Condition so that the prices match

    user_flights = flights_df[user_source & user_destination & cheapest_flight] # Assign any matching flights to user_flights
    if user_flights.size > 0:  # If there are any matching flights
        print(user_flights)    # Print them out
    else:
        print("Sorry, there were no flights matching the data you entered. Please try again.")

# Option 4 (Evan)
def find_min_dur():
    print("You chose option 4.")
    print('____________________________________')

# Option 5 (Gavin) COMPLETED
# search_specific_route() searches for the user's given route and returns a dataframe with any flights
# that have the exact same route as the user's input. If there is no matching route, then the user will be informed.
def search_specific_route():
    print("You chose option 5.")
    print('____________________________________')
    user_route = input('Enter your specific route (ex: BLR to BOM to AMD to DEL): ')
    full_route = user_route.replace('to', '?')  # Because the dataset is formatted with ? between each stop for some reason
    user_flights = flights_df[flights_df.Route == full_route] # Assign any matching flights to user_flights

    if user_flights.size > 0: # If there are any flights matching the route
        print(user_flights) # Prints any flight with the matching route from the dataset
    else:
        print("Sorry, there were no flights matching the data you entered. Please try again.")


# Option 6 (Evan)
def find_source_to_dest_by_date_and_price():
    print("You chose option 6.")


# Option 7 (Gavin) COMPLETED
# display_summary_of_airline() will display a summary for each airline that includes the cheapest
# and the most expensive flight per airline.
def display_summary_of_airline():
    print("You chose option 7.")
    print('____________________________________')
    num_of_unique_airlines = len(unique_airlines)
    for i in range(0, num_of_unique_airlines):  # For every unique airline
        max = 0  # Set max to 0 for initialization
        min = 1000000000  # Set min to arbitrary number for initialization
        for j in range(0, num_of_flights):  # For every flight
            if unique_airlines_list[i] == flights_df.Airline[j]:  # If the unique airline and the current flight's
                if flights_df.Price[j] > max:  # airline matches, and if the price of that flight is
                    max = flights_df.Price[j]  # greater than the current max, then set the max to that price.
                if flights_df.Price[j] < min:  # If the price is lower than the min, then set the min
                    min = flights_df.Price[j]  # to that price.

        print(f'{unique_airlines_list[i]} max: {max}')  # Print our airline and its respective max price
        print(f'{unique_airlines_list[i]} min: {min}')  # Print our airline and its respective min price
        if i != num_of_unique_airlines - 1:  # If statement for formatting to not print a dotted line at the very end
            print('------------------------------------')
    print('____________________________________')


# Option 8 (Evan)
def print_unique_cities():
    print("You chose option 8.")


# Option 9 (Gavin) COMPLETED
# print_unique_airlines() will print every unique airline from the dataset full of flights.
def print_unique_airlines():
    print("You chose option 9.")
    print("___________________________")
    print("Unique Airlines consist of:")
    print("---------------------------")
    for airline in unique_airlines:  # For every airline in the unique airline set, print it
        print(airline)
    print("___________________________")


# Option 10 (Evan)
def print_all_cities_by_airline():
    print("You chose option 10.")


######################
#        MAIN        #
######################

cont = True  # Condition to keep while loop going until told otherwise
while cont:  # While loop to continuously print the user's options and execute the option corresponding to user input
    print()
    print("1 - Search flights by source and destination in a specific day and month.")
    print("2 - Search flights by source city and departure time within specific date interval (ex: from 1/1 to 1/10).")
    print("3 - Find the cheapest flight from specific source to specific destination.")
    print("4 - Find the flight with minimum duration from specific source to specific destination.")
    print("5 - Search for specific route (ex: BLR to BOM to AMD to DEL.")
    print("6 - Find flights from specific source to specific destination within date interval and price interval.")
    print("7 - Display a summary per each Airline that includes the cheapest and most expensive flight per airline.")
    print("8 - Print all unique city names in the dataset.")
    print("9 - Print all unique airlines in the dataset.")
    print("10 - For each airline, print all cities (source or destination) the airline can reach.")
    print("11 - Exit")
    print()

    try:
        option = int(input("Choose an option: "))
    except ValueError:
        print("Invalid value. Integers between 1 and 10 only please.")
        continue

    if option == 1:
        search_by_source_destination()
    elif option == 2:
        search_by_source_departure_by_date()
    elif option == 3:
        find_cheapest()
    elif option == 4:
        find_min_dur()
    elif option == 5:
        search_specific_route()
    elif option == 6:
        find_source_to_dest_by_date_and_price()
    elif option == 7:
        display_summary_of_airline()
    elif option == 8:
        print_unique_cities()
    elif option == 9:
        print_unique_airlines()
    elif option == 10:
        print_all_cities_by_airline()
    elif option == 11:
        print("Exiting...")
        cont = False
    else:
        print("Invalid option. Please try again.")
