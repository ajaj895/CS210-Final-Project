# Link to assignment: https://westernonline.wiu.edu/d2l/le/content/169197/viewContent/2469388/View?ou=169197
# Data used: https://www.kaggle.com/vinaypratap/flight-price

# Authors: Evan Colwell
#          Gavin Horner
# School: Western Illinois University
# Class: CS210: Python for Data Exploration

import pandas as pd

flights_df = pd.read_csv("Data_Train.csv")  # Open our data file and store it as a data frame for use within the methods
unique_airlines = set(flights_df.Airline)  # A set of unique airlines declared early for use in option 9.
unique_airlines_list = list(unique_airlines)  # A list of unique airlines for easy index access declared early for use in option 7
num_of_flights = len(flights_df.Airline) # Length of the dataset for use in any option 1 and 7

pd.set_option('display.width', 320)
pd.set_option("display.max_columns", 11)  # All necessary for proper formatting in the Run output box
pd.set_option("display.max_rows", 10683)  # Comment out as needed

# Option 1 (Gavin) IN PROGRESS
def search_by_source_destination():
    print("You chose option 1.")
    source = input("Please enter a source: ")
    destination = input("Please enter a destination: ")
    day = input("Please enter a day: ")
    month = input("Please enter a month: ")

    rows = []
    for i in range(0, num_of_flights):
        flight_day, flight_month, flight_year = flights_df.Date_of_Journey[i].split('/')
        if flights_df.Source[i] == source:
            if flights_df.Destination[i] == destination:
                if flight_day == day:
                    if flight_month == month:
                        rows.append([flights_df.iloc[[i]]])


# Option 2 (Evan)
def search_by_source_departure_by_date():
    print("You chose option 2.")


# Option 3 (Gavin)
def find_cheapest():
    print("You chose option 3.")


# Option 4 (Evan)
def find_min_dur():
    print("You chose option 4.")


# Option 5 (Gavin) COMPLETED
def search_specific_route():
    print("You chose option 5.")
    print('____________________________________')
    user_route = input('Enter your specific route (ex: BLR to BOM to AMD to DEL): ')
    full_route = user_route.replace('to', '?')  # Because the dataset is formatted with ? between each stop for some reason
    print(flights_df[flights_df.Route == full_route]) # Prints any flight with the matching route from the dataset


# Option 6 (Evan)
def find_source_to_dest_by_date_and_price():
    print("You chose option 6.")


# Option 7 (Gavin) COMPLETED
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
                    max = flights_df.Price[j]  # greater than the current max, then set the max to
                    # that price.
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
