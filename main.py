# Link to assignment: https://westernonline.wiu.edu/d2l/le/content/169197/viewContent/2469388/View?ou=169197

# Option 1
def search_by_source_destination():
    print("You chose option 1.")


# Option 2
def search_by_source_departure_by_date():
    print("You chose option 2.")


# Option 3
def find_cheapest():
    print("You chose option 3.")


# Option 4
def find_min_dur():
    print("You chose option 4.")


# Option 5
def search_specific_route():
    print("You chose option 5.")


# Option 6
def find_source_to_dest_by_date_and_price():
    print("You chose option 6.")


# Option 7
def display_summary_of_airline():
    print("You chose option 7.")


# Option 8
def print_unique_cities():
    print("You chose option 8.")


# Option 9
def print_unique_airlines():
    print("You chose option 9.")


# Option 10
def print_all_cities_by_airline():
    print("You chose option 10.")


######################
#        MAIN        #
######################
cont = True
while cont:
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
        break
    else:
        print("Invalid option. Please try again.")
        continue