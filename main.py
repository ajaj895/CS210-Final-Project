# Link to assignment: https://westernonline.wiu.edu/d2l/le/content/169197/viewContent/2469388/View?ou=169197
# Data used: https://www.kaggle.com/vinaypratap/flight-price

# Authors: Evan Colwell
#          Gavin Horner
# Date: November 2020
# School: Western Illinois University
# Class: CS210: Python for Data Exploration

import re  # Needed for option 4
import pandas as pd
import numpy as np

flights_df = pd.read_csv("Data_Train.csv")  # Open our data file and store it as a data frame for use within the methods
unique_airlines = set(flights_df.Airline)  # A set of unique airlines declared early for use in option 9.
unique_airlines_list = list(
    unique_airlines)  # A list of unique airlines for easy index access declared early for use in option 7
num_of_flights = len(flights_df.Airline)  # Length of the dataset for use in option 1 and 7
unique_start_cities = list(flights_df.Source)  # Used for option 8
unique_dest_cities = list(flights_df.Destination)  # Used for option 8

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

    date = f'{day}/{month}/2019'  # Declare our date, 2019 static as all entries are from 2019
    user_source = flights_df.Source == source  # Condition so the sources match
    user_destination = flights_df.Destination == destination  # Condition so the destinations match
    user_date = flights_df.Date_of_Journey == date  # Condition so the dates match

    user_flights = flights_df[user_source & user_destination & user_date]  # Assign any matching flights to user_flights

    if user_flights.size > 0:  # If there are any matching flights
        print(user_flights)  # Print any flights matching the conditions
    else:
        print("Sorry, there were no flights matching the data you entered. Please try again.")


# Option 2 (Evan) - Completed
# search_by_source_departure_by_date() searches for flights based on starting city and date range
# Handles errors from the user and will not continue until the user enters the correct input
def search_by_source_departure_by_date():
    print("You chose option 2.")
    print('____________________________________')
    start_city = input('Enter the starting city: ').title()  # Makes sure that the format is not a problem

    # --- Error Handling with input ---
    while 1:
        error = False
        start_range = input('Enter the first day in your range (month/day): ')
        end_range = input('Enter the last day in your range (month/day): ')
        temp_start_list = start_range.split('/')
        temp_end_list = end_range.split('/')

        if not len(temp_start_list) == 2:  # Checks for if the date size is an unexpected value.
            print('Error! Start date range needs to be a proper month/day date (ex. 1/10, or 5/18).')
            continue
        if not len(temp_end_list) == 2:
            print('Error! Ending date range needs to be a proper month/day date (ex. 1/10, or 5/18).')
            continue

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
        for i in range(int(temp_start_list[1]), int(temp_end_list[1]) + 1):  # Inclusive
            day = f'{i}'
            if i < 10:  # Formats the day
                day = f'0{i}'
            str_date = [day, month, '2019']  # day month year, the / is not needed to store
            date_range.append(str_date)
    else:
        for m in range(int(temp_start_list[0]), int(temp_end_list[0]) + 1):  # For each month inclusive
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
                for d in range(1, int(temp_end_list[1]) + 1):
                    day = f'{d}'
                    if d < 10:  # Formats the day
                        day = f'0{d}'
                    str_date = [day, month, '2019']  # day month year, the / is not needed to store
                    date_range.append(str_date)
            else:  # Any month in-between start and end month
                for d in range(1, 32):
                    day = f'{d}'
                    if d < 10:  # Formats the day
                        day = f'0{d}'
                    str_date = [day, month, '2019']  # day month year, the / is not needed to store
                    date_range.append(str_date)

    hit = False  # Used for telling if flights were found or not
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


#  Option 2 (cont.) (Evan)
#  Overloaded version of option 2, used to return a list of dataframe locations used in option 6
def search_by_source_departure_by_date_list(start_city, start_date_list, end_date_list):
    date_range = []  # List of dates, each element is list of a date ['day', 'month', 'year']
    found_flights = []

    # --- date_range formatting ---
    if start_date_list[0] == end_date_list[0]:  # Same month
        if int(start_date_list[0]) < 10:  # Formats the month if less than 10 (ex 05, or 01)
            month = f'0{start_date_list[0]}'
        else:
            month = start_date_list[0]
        for i in range(int(start_date_list[1]), int(end_date_list[1]) + 1):  # Inclusive
            day = f'{i}'
            if i < 10:  # Formats the day
                day = f'0{i}'
            str_date = [day, month, '2019']  # day month year, the / is not needed to store
            date_range.append(str_date)
    else:
        for m in range(int(start_date_list[0]), int(end_date_list[0]) + 1):  # For each month inclusive
            if int(start_date_list[0]) < 10:  # Formats the month if less than 10 (ex 05, or 01)
                month = f'0{m}'
            else:
                month = f'{m}'
            if m == int(start_date_list[0]):  # The start month
                for d in range(int(start_date_list[1]), 32):
                    day = f'{d}'
                    if d < 10:  # Formats the day
                        day = f'0{d}'
                    str_date = [day, month, '2019']  # day month year, the / is not needed to store
                    date_range.append(str_date)
            elif m == int(end_date_list[0]):  # If the end month has been reached, inclusive
                for d in range(1, int(end_date_list[1]) + 1):
                    day = f'{d}'
                    if d < 10:  # Formats the day
                        day = f'0{d}'
                    str_date = [day, month, '2019']  # day month year, the / is not needed to store
                    date_range.append(str_date)
            else:  # Any month in-between start and end month
                for d in range(1, 32):
                    day = f'{d}'
                    if d < 10:  # Formats the day
                        day = f'0{d}'
                    str_date = [day, month, '2019']  # day month year, the / is not needed to store
                    date_range.append(str_date)
    # --- End of date_range formatting ---

    for i in range(0, num_of_flights):
        if flights_df.Source[i] == start_city:
            # If the city is located, then check for the date match
            check_date = flights_df.Date_of_Journey[i].split('/')
            for date in date_range:  # For each date in the list is better than each flight in the DB
                if check_date[1] == date[1]:  # Check month
                    if check_date[0] == date[0]:  # Check day
                        found_flights.append(i)  # Adds to the found flight list

    return found_flights  # Returns an empty list if nothing is found


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
            if flights_df.Destination[i] == destination:  # And the destinations match
                if flights_df.Price[i] < cheapest:  # And the price is lower than the current cheapest
                    cheapest = flights_df.Price[i]  # Reassign cheapest to be that price

    user_source = flights_df.Source == source  # Condition so that the sources match
    user_destination = flights_df.Destination == destination  # Condition so that the destinations match
    cheapest_flight = flights_df.Price == cheapest  # Condition so that the prices match

    user_flights = flights_df[user_source & user_destination & cheapest_flight]  # Assign any matching flights to user_flights
    if user_flights.size > 0:  # If there are any matching flights
        print(user_flights)  # Print them out
    else:
        print("Sorry, there were no flights matching the data you entered. Please try again.")


# Option 4 (Evan) - Complete
# find_min_dur finds the minimum length flight from source to destination.
def find_min_dur():
    print("You chose option 4.")
    print('____________________________________')
    start_city = input('Enter the starting city: ').title()  # Makes sure that the format is not a problem
    end_city = input('Enter the destination city: ').title()
    min_flight = ['100', '50']  # Arbitrary high number (first number is hours, second is minutes)
    min_flight_num = -1  # An int used later to retrieve the minimum flight
    # --- Flight finding logic ---
    for flight in range(0, num_of_flights):
        if flights_df.Source[flight] == start_city and flights_df.Destination[flight] == end_city:
            duration = flights_df.Duration[flight].split()  # Slicing of the duration string
            if len(duration) == 1:  # If the duration has only hours or minutes
                if re.fullmatch(r'\d+h', duration[0]):  # If only hours duration
                    hours = re.sub(r'h', '', duration[0])
                    if int(hours) < int(min_flight[0]) and int(min_flight[1]) > 0:
                        # If faster flight found, replaces the current minimum with this minimum flight
                        min_flight[0] = hours
                        min_flight[1] = 0
                        min_flight_num = flight
                else:
                    minutes = re.sub(r'm', '', duration[0])
                    if int(minutes) < int(min_flight[1]) and int(min_flight[0]) > 0:
                        # If faster flight found, replaces the current minimum with this minimum flight
                        min_flight[0] = 0
                        min_flight[1] = minutes
                        min_flight_num = flight
            else:
                hours = re.sub(r'h', '', duration[0])
                minutes = re.sub(r'm', '', duration[1])
                if int(hours) < int(min_flight[0]):
                    # If faster flight found, replaces the current minimum with this minimum flight
                    min_flight[0] = hours
                    min_flight[1] = minutes
                    min_flight_num = flight
                elif hours == min_flight[0] and int(minutes) < int(min_flight[1]):
                    # If faster flight found, replaces the current minimum with this minimum flight
                    min_flight[0] = hours
                    min_flight[1] = minutes
                    min_flight_num = flight
    # --- End of flight finding logic ---
    if min_flight_num > -1:  # If a flight was found
        print('____________________________________')
        print(flights_df.loc[min_flight_num])
        print('____________________________________')
    else:  # If no flights were found
        print('____________________________________')
        print('No flights found!')
        print('____________________________________')


# Option 5 (Gavin) COMPLETED
# search_specific_route() searches for the user's given route and returns a dataframe with any flights
# that have the exact same route as the user's input. If there is no matching route, then the user will be informed.
def search_specific_route():
    print("You chose option 5.")
    print('____________________________________')
    user_route = input('Enter your specific route (ex: BLR to BOM to AMD to DEL): ')
    full_route = user_route.replace('to',
                                    '?')  # Because the dataset is formatted with ? between each stop for some reason
    user_flights = flights_df[flights_df.Route == full_route]  # Assign any matching flights to user_flights

    if user_flights.size > 0:  # If there are any flights matching the route
        print(user_flights)  # Prints any flight with the matching route from the dataset
    else:
        print("Sorry, there were no flights matching the data you entered. Please try again.")


# Option 6 (Evan) - Completed
# Finds a flight by source/destination/date and price
def find_source_to_dest_by_date_and_price():
    print("You chose option 6.")
    print('____________________________________')
    final_check_list = []  # Used for the flights found by destination, check by price still needed
    found_flights = []  # Used for found flights

    start_city = input('Enter the starting city: ').title()  # Makes sure that the format is not a problem
    destination = input('Enter the destination: ').title()

    # --- Error Handling with input ---
    while 1:
        error = False
        start_range = input('Enter the first day in your range (month/day): ')
        end_range = input('Enter the last day in your range (month/day): ')
        temp_start_list = start_range.split('/')
        temp_end_list = end_range.split('/')

        if not len(temp_start_list) == 2:  # Checks for if the date size is an unexpected value.
            print('Error! Start date range needs to be a proper month/day date (ex. 1/10, or 5/18).')
            continue
        if not len(temp_end_list) == 2:
            print('Error! Ending date range needs to be a proper month/day date (ex. 1/10, or 5/18).')
            continue


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
    # --- End of date range error handling ---
    # --- Price handling ---
    price_min = 0
    price_max = 0
    while 1:
        try:  # For minimum handling
            price_min = int(input('Enter the minimum price in your range (only numbers and in Indian Rupees): '))
        except ValueError:
            print('Error! Numbers only for the min price.')
            continue
        if price_max < 0:
            print('Error! Price minimum can\'t be negative.')
            continue
        try:  # For maximum handling
            price_max = int(input('Enter the maximum price in your range (only numbers and in Indian Rupees): '))
        except ValueError:
            print('Error! Numbers only for the max price.')
            continue
        if price_max < 0:
            print('Error! Price maximum can\'t be negative.')
            continue
        else:
            break
    # --- End of price handling ---
    # --- End of error handling ---

    # Finds start city and date range
    found_list = search_by_source_departure_by_date_list(start_city, temp_start_list, temp_end_list)

    for hit in found_list:  # Filters by destination
        if flights_df.Destination[hit] == destination:
            final_check_list.append(hit)

    for hit in final_check_list:  # Filters by price
        if price_min < int(flights_df.Price[hit]) < price_max:
            found_flights.append(hit)

    if len(found_flights) > 0:  # If flights were found
        for flight in found_flights:
            print('____________________________________')
            print(flights_df.loc[flight])
            print('____________________________________')
    else:
        print('____________________________________')
        print('No flights found!')
        print('____________________________________')


# Option 7 (Gavin) COMPLETED
# display_summary_of_airline() will display a summary for each airline that includes the cheapest
# and the most expensive flight per airline.
def display_summary_of_airline():
    print("You chose option 7.")
    print('____________________________________')
    num_of_unique_airlines = len(unique_airlines)
    cheapest = np.zeros(num_of_unique_airlines, dtype=int) # Holding array of cheapest flights
    most_expensive = np.zeros(num_of_unique_airlines, dtype=int) # Holding array of most expensive flights
    for i in range(0, num_of_unique_airlines):  # For every unique airline
        max = 0  # Set max to 0 for initialization
        min = 1000000000  # Set min to arbitrary number for initialization
        for j in range(0, num_of_flights):  # For every flight
            if unique_airlines_list[i] == flights_df.Airline[j]:  # If the unique airline and the current flight's
                if flights_df.Price[j] > max:  # airline matches, and if the price of that flight is
                    max = flights_df.Price[j]  # greater than the current max, then set the max to that price.
                if flights_df.Price[j] < min:  # If the price is lower than the min, then set the min
                    min = flights_df.Price[j]  # to that price.

        cheapest[i] = min  # Assign them as min is found
        most_expensive[i] = max # Assign them as max is found

    for k in range(0, num_of_unique_airlines): # For every unique airline
        flight_airline = flights_df.Airline == unique_airlines_list[k]  # Condition for the airline
        most_expensive_flight = flights_df.Price == most_expensive[k]   # Condition for the most expensive flight
        max_flights = flights_df[flight_airline & most_expensive_flight] # All max flights for that airline
        for index in max_flights.index.values:  # For every index of the max flight
            print(flights_df.iloc[index]) # Print it out and all its information

        cheapest_flight = flights_df.Price == cheapest[k]  # Condition for cheapest flight
        min_flights = flights_df[flight_airline & cheapest_flight] # All min flights for that airline
        for index in min_flights.index.values:  # For every index of the max flight
            print(flights_df.iloc[index]) # Print it out and all its information


        df = pd.DataFrame({'Airline': [], 'Date_of_Journey': [], 'Source': [], 'Destination': [], 'Route': [],
                           'Dep_Time': [], 'Arrival_Time': [], 'Duration': [], 'Total_Stops': [], 'Additional_Info': [],
                           'Price': []})



# Option 8 (Evan) - Complete
# print_unique_cities() will print out a sorted list of unique cities for the flights both source and destination.
def print_unique_cities():
    print("You chose option 8.")
    print('____________________________________')

    unique_cities = []

    for city in range(0, len(unique_start_cities)):  # For source cities
        found = False
        for i in range(0, len(unique_cities)):  # Checks current unique list of cities
            if unique_cities[i] == unique_start_cities[city]:
                found = True
                break
        if not found:
            unique_cities.append(unique_start_cities[city])
    for city in range(0, len(unique_dest_cities)):  # For destination cities
        found = False
        for i in range(0, len(unique_cities)):  # Checks current unique list of cities
            if unique_cities[i] == unique_dest_cities[city]:
                found = True
                break
        if not found:
            unique_cities.append(unique_dest_cities[city])
    unique_cities.sort()  # Sorts the list just for looks
    print('Unique cities: ')
    print(unique_cities)
    print('____________________________________')


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


# Option 10 (Evan) - Complete
# print_all_cities_by_airline() prints out all the cities serviced by airline in the dataset
def print_all_cities_by_airline():
    print("You chose option 10.")
    print('____________________________________')

    for airline in unique_airlines_list:
        unique_cities = []  # Keeps tabs on what city has been seen before
        flight_list = []
        for flight in range(0, num_of_flights):  # Not good but the best idea I could think of at the time
            if flights_df.Airline[flight] == airline:  # If airline is found
                found_source = False  # Used for if the source has already been seen before
                found_destination = False  # Used for if the destination has already been seen before
                for i in range(0, len(unique_cities)):  # Checks every flight in the dataset
                    if unique_cities[i] == flights_df.Source[flight]:
                        found_source = True
                    if unique_cities[i] == flights_df.Destination[flight]:
                        found_destination = True
                    if found_source and found_destination:
                        break
                if not found_source:  # When the source is new
                    flight_list.append(flights_df.Source[flight])
                    unique_cities.append(flights_df.Source[flight])
                if not found_destination:  # When the destination is new
                    flight_list.append(flights_df.Destination[flight])
                    unique_cities.append(flights_df.Destination[flight])

        flight_list.sort()
        print('Cities serviced by', airline, flight_list)
        print('____________________________________')


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
        print("Invalid value. Integers between 1 and 11 only please.")
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
