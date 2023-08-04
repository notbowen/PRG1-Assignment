# Name: Hu Bowen (S10255800B)
# Date: 1 Aug 2023
# Last Modified: 2 Aug 2023
#
# basic.py
# Implementation of the basic & advanced requirements in
# Assignment of PRG1, 2023

# Imports
from utils.input import validate_input_str, validate_input_num
from utils.carpark import get_carpark_information
from utils.carpark import get_all_carpark_info, associate_carpark_info, parse_carpark_information
from utils.carpark import get_timestamp, set_timestamp
from utils.files import load_file, write_file

# Global variables
ran_opt_3 = False


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
[8]  Display All Carparks at Given Location
[9]  Display Carpark with the Most Parking Lots
[10] Create an Output File with Sorted Carpark Availability with Addresses
[0]  Exit"""

    print(display_str)
    choice = validate_input_num(
        "Enter your option: ", list(range(1, 11)) + [0])
    return choice


def option_1() -> None:
    """Function to display total number of carparks in carpark_info"""
    carpark_info = get_carpark_information()
    total_cps = len(carpark_info)

    print("Option 1: Display Total Number of Carparks in 'carpark-information.csv'")
    print("Total Number of carparks in 'carpark-information.csv': {}".format(total_cps))


def option_2() -> None:
    """Function to display all basement carparks"""
    # Print option
    print("Option 2: Display All Basement Carparks in 'carpark-information.csv'")

    # Get basement carparks
    carpark_info = get_carpark_information()
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
    global ran_opt_3

    # Prints out option header
    print("Option 3: Read Carpark Availability Data File")

    # Get filename from user
    filename = validate_input_str(
        "Enter the file name: ",
        "carpark-availability-v1.csv",
        "carpark-availability-v2.csv"
    )

    # Get the carpark availability
    cp_availability = load_file(filename)

    # Get and set timestamp
    timestamp = cp_availability.pop(0)
    set_timestamp(timestamp)

    # Get the carpark information
    cp_info = get_carpark_information()

    # Associate the carpark information & availability and get timestamp
    cp_availability = parse_carpark_information(cp_availability)
    associate_carpark_info(cp_availability, cp_info)

    # Prints out header
    print(timestamp)

    # Toggle option 3 ran
    ran_opt_3 = True


def option_4() -> None:
    """Function to print the total number of carparks in the file read"""
    # Print header
    print("Option 4: Print Total Number of Carparks in the File Read in [3]")

    # Get total number
    carpark_availability = get_all_carpark_info()
    total = len(carpark_availability)

    # Display total number
    print("Total Number of Carparks in the File: {}".format(total))


def option_5() -> None:
    """Function to display all carparks that are full"""
    # Print header
    print("Option 5: Display Carparks without Available Lots")

    # Get carparks without lots
    carpark_availability = get_all_carpark_info()
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
    percentage = validate_input_num(
        "Enter the percentage required: ", range(0, 101))

    # Get carparks that are above or equal to that percentage
    carpark_availability = get_all_carpark_info()
    cps_available = [
        cp for cp in carpark_availability if cp["Percentage"] >= percentage]

    # Loop through and display
    print("{:10} {:10} {:14} {:10}".format("Carpark No",
          "Total Lots", "Lots Available", "Percentage"))
    for cp in cps_available:
        num = cp["Carpark Number"]
        total = cp["Total Lots"]
        available = cp["Lots Available"]
        percentage = cp["Percentage"]

        print("{:10} {:>10} {:>14} {:10.1f}".format(
            num, total, available, percentage))

    # Display total length
    print("Total number: {}".format(len(cps_available)))


def option_7() -> None:
    """Function to display carparks with x% availibility"""
    # Print header
    print("Option 7: Display Addresses of Carparks With At Least x% Available Lots")

    # Get percentage required
    percentage = validate_input_num(
        "Enter the percentage required: ", range(0, 101))

    # Get carparks that are above or equal to that percentage
    carpark_availability = get_all_carpark_info()
    cps_available = [
        cp for cp in carpark_availability if cp["Percentage"] >= percentage]

    # Loop through and display
    print("{:10} {:10} {:14} {:10}   {}".format("Carpark No",
          "Total Lots", "Lots Available", "Percentage", "Address"))
    for cp in cps_available:
        num = cp["Carpark Number"]
        total = cp["Total Lots"]
        available = cp["Lots Available"]
        percentage = cp["Percentage"]
        address = cp["Address"]

        print("{:10} {:>10} {:>14} {:10.1f}   {}".format(
            num, total, available, percentage, address))

    # Display total length
    print("Total number: {}".format(len(cps_available)))


def option_8() -> None:
    """Function to display all carparks at a given location"""
    print("Option 8: Display All Carparks at Given Location")

    # Get location input from user
    location = input("Please enter the location to search for: ")
    location = location.upper()

    # Get all carpark data
    carparks = get_all_carpark_info()

    # Filter carpark data by address
    carparks_at_location = [cp for cp in carparks if location in cp["Address"]]

    # Display location not found if no carparks are found
    if len(carparks_at_location) == 0:
        print("No carparks found at location: {}".format(location))
        return

    # Format and display all carparks at location
    print("{:10} {:10} {:14} {:10}   {}".format("Carpark No",
          "Total Lots", "Lots Available", "Percentage", "Address"))
    for cp in carparks_at_location:
        num = cp["Carpark Number"]
        total = cp["Total Lots"]
        available = cp["Lots Available"]
        percentage = cp["Percentage"]
        address = cp["Address"]

        print("{:10} {:>10} {:>14} {:10.1f}   {}".format(
            num, total, available, percentage, address))

    # Display length
    print("Total number: {}".format(len(carparks_at_location)))


def option_9() -> None:
    """Function to display carparks with the most parking lots"""

    # Get all carparks
    carparks = get_all_carpark_info()

    # Get the highest carpark
    highest_cp = carparks[0]
    for cp in carparks:
        if cp["Total Lots"] > highest_cp["Total Lots"]:
            highest_cp = cp

    # Display the carpark information
    print("{:10} {:10} {:14} {:10}   {}".format("Carpark No",
          "Total Lots", "Lots Available", "Percentage", "Address"))

    num = highest_cp["Carpark Number"]
    total = highest_cp["Total Lots"]
    available = highest_cp["Lots Available"]
    percentage = highest_cp["Percentage"]
    address = highest_cp["Address"]

    print("{:10} {:>10} {:>14} {:10.1f}   {}".format(
        num, total, available, percentage, address))


def option_10() -> None:
    """Function to create output file with sorted carpark info"""
    # Get all carparks
    carparks = get_all_carpark_info()

    # Sort by available lots
    # Line taken from: https://stackoverflow.com/questions/72899/how-to-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary-in-python
    sorted_carpark = sorted(carparks, key=lambda cp: int(cp["Lots Available"]))

    # Get timestamp
    timestamp = get_timestamp()

    # Loop through sorted carparks and write to file
    content = ""

    # Write timestamp and headers
    content += timestamp + '\n'
    content += "Carpark Number,Total Lots,Lots Available,Address\n"

    # Write the sorted data to the csv file
    for cp in sorted_carpark:
        data = [cp["Carpark Number"], cp["Total Lots"],
                cp["Lots Available"], cp["Address"]]
        content += ",".join(data)
        content += '\n'

    # Apply changes to the csv file
    write_file("carpark-availability-with-addresses.csv", content)

    # Display number of lines written
    lines = len(sorted_carpark) + 2
    print("Lines written: {}".format(lines))

    # Display filename
    print("Wrote to file: ./res/carpark-availability-with-addresses.csv")


def main() -> None:
    # Load carpark information
    get_carpark_information()

    # Mainloop
    while True:
        option = main_menu()  # Get option from user
        print()  # Padding

        # Quit if user inputs 0
        if option == 0:
            break

        # Check if option 3 has been ran for options 4..=7
        if option > 3 and not ran_opt_3:
            print("Please run option 3 first!")
            continue

        # Run specified option and wait for user to press enter to continue
        eval("option_{}()".format(option))