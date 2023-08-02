# Name: Hu Bowen (S10255800B)
# Date: 1 Aug 2023
#
# basic.py
# Implementation of the basic requirements in
# Assignment of PRG1, 2023

# Imports
from utils.input import validate_num, validate_str
from utils.files import load_file, parse_carpark_information
from utils.carpark import get_cp_percentage, cache_cp_address

# Initialise global variables
carpark_info = None
carpark_availability = None
carpark_cache = None

# Functions
def main_menu() -> int:
    """Displays the main menu and returns the choice the user gave

    Returns:
        int: Choice that user gave
    """

    display_str = \
        """
MENU
====
[1]  Display Total Number of Carparks in 'carpark-information.csv'
[2]  Display All Basement Carparks in 'carpark-information.csv'
[3]  Read Carpark Availability Data File
[4]  Print Total Number of Carparks in the File Read in [3]
[5]  Display Carparks Without Available Lots
[6]  Display Carparks With At Least x% Available Lots
[7]  Display Addresses of Carparks With At Least x% Available Lots 
[0]  Exit"""

    print(display_str)
    choice = validate_num("Enter your option: ", list(range(1, 8)) + [0])
    return choice


def option_1() -> None:
    """Function to display total number of carparks in carpark_info"""
    total_cps = len(carpark_info)

    print("Option 1: Display Total Number of Carparks in 'carpark-information.csv'")
    print("Total Number of carparks in 'carpark-information.csv': {}".format(total_cps))


def option_2() -> None:
    """Function to display all basement carparks"""
    # Print option
    print("Option 2: Display All Basement Carparks in 'carpark-information.csv'")

    # Get basement carparks
    basements = [cp for cp in carpark_info
                 if cp["Carpark Type"] == "BASEMENT CAR PARK"]

    # Loop and display them
    print("{:10} {:20} {}".format("Carpark No", "Carpark Type", "Address"))
    for basement in basements:
        # Extract neccessary info
        num = basement["Carpark Number"]
        cp_type = basement["Carpark Type"]
        addr = basement["Address"]

        # Print out info
        print("{:10} {:20} {}".format(num, cp_type, addr))

    # Display total number of basement CPs
    print("Total number: {}".format(len(basements)))


def option_3() -> None:
    """Reads the user-specified file and loads the data to carpark_availability"""
    global carpark_availability, carpark_cache

    # Prints out option header
    print("Option 3: Read Carpark Availability Data File")

    filename = validate_str(
        "Enter the file name: ",
        "carpark-availability-v1.csv",
        "carpark-availability-v2.csv"
    )

    carpark_availability = load_file(filename)
    timestamp = carpark_availability.pop(0)
    carpark_availability = parse_carpark_information(carpark_availability)

    # Calculate and cache the carpark availability and addresses
    carpark_cache = get_cp_percentage(carpark_availability)
    cache_cp_address(carpark_info, carpark_cache)

    # Prints out header
    print(timestamp)


def option_4() -> None:
    """Function to print the total number of carparks in the file read"""
    # Print header
    print("Option 4: Print Total Number of Carparks in the File Read in [3]")

    # Get total number
    total = len(carpark_availability)

    # Display total number
    print("Total Number of Carparks in the File: {}".format(total))


def option_5() -> None:
    """Function to display all carparks that are full"""
    # Print header
    print("Option 5: Display Carparks without Available Lots")

    # Get carparks without lots
    empty_cps = [
        cp for cp in carpark_availability if cp["Lots Available"] == '0']

    # Loop through empty carparks an print their number
    for carpark in empty_cps:
        print("Carpark Number: {}".format(carpark["Carpark Number"]))

    # Print total length
    print("Total number: {}".format(len(empty_cps)))


def option_6() -> None:
    """Function to display carparks with x% availibility"""
    # Print header
    print("Option 6: Display Carparks With At Least x% Available Lots")

    # Get percentage required
    percentage = validate_num("Enter the percentage required: ", range(0, 101))

    # Get carparks that are above or equal to that percentage
    cps_available = [
        cp for cp in carpark_cache if cp["Percentage"] >= percentage]

    # Loop through and display
    print("{:10} {:10} {:10} {:10}".format("Carpark No",
          "Total Lots", "Lots Available", "Percentage"))
    for cp in cps_available:
        num = cp["Carpark Number"]
        total = cp["Total Lots"]
        available = cp["Lots Available"]
        percentage = cp["Percentage"]

        print("{:10} {:>10} {:>10} {:10.1f}".format(
            num, total, available, percentage))

    # Display total length
    print("Total number: {}".format(len(cps_available)))


def option_7() -> None:
    """Function to display carparks with x% availibility"""
    # Print header
    print("Option 7: Display Addresses of Carparks With At Least x% Available Lots")

    # Get percentage required
    percentage = validate_num("Enter the percentage required: ", range(0, 101))

    # Get carparks that are above or equal to that percentage
    cps_available = [
        cp for cp in carpark_cache if cp["Percentage"] >= percentage]

    # Loop through and display
    print("{:10} {:10} {:10} {:10} {}".format("Carpark No",
          "Total Lots", "Lots Available", "Percentage", "Address"))
    for cp in cps_available:
        num = cp["Carpark Number"]
        total = cp["Total Lots"]
        available = cp["Lots Available"]
        percentage = cp["Percentage"]
        address = cp["Address"]

        print("{:10} {:>10} {:>10} {:10.1f} {}".format(
            num, total, available, percentage, address))

    # Display total length
    print("Total number: {}".format(len(cps_available)))


def main() -> None:
    # Load carpark information
    global carpark_info
    carpark_info = load_file("carpark-information.csv")
    carpark_info = parse_carpark_information(carpark_info)

    # Mainloop
    while True:
        option = main_menu()  # Get option from user
        print()  # Padding

        # Quit if user inputs 0
        if option == 0:
            break

        # Check if option 3 has been ran for options 4..=7
        if option > 3 and carpark_availability is None:
            print("Please run option 3 first!")
            continue

        # Run specified option and wait for user to press enter to continue
        eval("option_{}()".format(option))
