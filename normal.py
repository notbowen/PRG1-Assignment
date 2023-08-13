# Name: Hu Bowen (S10255800B)
# Date: 1 Aug 2023
# Last Modified: 2 Aug 2023
#
# basic.py
# Implementation of the basic & advanced requirements in
# Assignment of PRG1, 2023

from typing import List, Dict

from utils.carpark import associate_carpark_info, parse_carpark_information
from utils.carpark import get_carpark_information
from utils.files import load_file, write_file
from utils.input import validate_input_str, validate_input_num


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


def option_1(carpark_info: List[Dict[str, str]], _: List[Dict[str, str]]) -> None:
    """Function to display total number of carparks in carpark_info"""
    total_cps = len(carpark_info)

    print("Option 1: Display Total Number of Carparks in 'carpark-information.csv'")
    print("Total Number of carparks in 'carpark-information.csv': {}".format(total_cps))


def option_2(carpark_info: List[Dict[str, str]], _: List[Dict[str, str]]) -> None:
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
        addr = basement["Address"].strip("\"")

        # Print out info
        print("{:10} {:20} {}".format(num, cp_type, addr))

    # Display total number of basement CPs
    print("Total number: {}".format(len(basements)))


def option_3(
        carpark_info: List[Dict[str, str]],
        _: List[Dict[str, str]]
) -> tuple[str, list[dict[str, str]]]:
    """Reads the user-specified file and loads the data to carpark_availability"""
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

    # Associate the carpark information & availability and get timestamp
    cp_availability = parse_carpark_information(cp_availability)
    all_cp_info = associate_carpark_info(cp_availability, carpark_info)

    # Prints out header
    print(timestamp)

    # Return associated carpark info
    return timestamp, all_cp_info


def option_4(_: List[Dict[str, str]], all_cp_info: List[Dict[str, str]]) -> None:
    """Function to print the total number of carparks in the file read"""
    # Print header
    print("Option 4: Print Total Number of Carparks in the File Read in [3]")

    # Get total number
    total = len(all_cp_info)

    # Display total number
    print("Total Number of Carparks in the File: {}".format(total))


def option_5(_: List[Dict[str, str]], all_cp_info: List[Dict[str, str]]) -> None:
    """Function to display all carparks that are full"""
    # Print header
    print("Option 5: Display Carparks without Available Lots")

    # Get carparks without lots
    empty_cps = [
        cp for cp in all_cp_info if cp["Lots Available"] == '0']

    # Loop through empty carparks and print their number
    for carpark in empty_cps:
        print("Carpark Number: {}".format(carpark["Carpark Number"]))

    # Print total length
    print("Total number: {}".format(len(empty_cps)))


def option_6(_: List[Dict[str, str]], all_cp_info: List[Dict[str, str]]) -> None:
    """Function to display carparks with x% availability"""
    # Print header
    print("Option 6: Display Carparks With At Least x% Available Lots")

    # Get percentage required
    percentage = validate_input_num(
        "Enter the percentage required: ", range(0, 101))

    # Get carparks that are above or equal to that percentage
    cps_available = [
        cp for cp in all_cp_info if cp["Percentage"] >= percentage]

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


def option_7(_: List[Dict[str, str]], all_cp_info: List[Dict[str, str]]) -> None:
    """Function to display carparks with x% availability"""
    # Print header
    print("Option 7: Display Addresses of Carparks With At Least x% Available Lots")

    # Get percentage required
    percentage = validate_input_num(
        "Enter the percentage required: ", range(0, 101))

    # Get carparks that are above or equal to that percentage
    cps_available = [
        cp for cp in all_cp_info if cp["Percentage"] >= percentage]

    # Loop through and display
    print("{:10} {:10} {:14} {:10}   {}".format("Carpark No",
                                                "Total Lots", "Lots Available", "Percentage", "Address"))
    for cp in cps_available:
        num = cp["Carpark Number"]
        total = cp["Total Lots"]
        available = cp["Lots Available"]
        percentage = cp["Percentage"]
        address = cp["Address"].strip("\"")

        print("{:10} {:>10} {:>14} {:10.1f}   {}".format(
            num, total, available, percentage, address))

    # Display total length
    print("Total number: {}".format(len(cps_available)))


def option_8(_: List[Dict[str, str]], all_cp_info: List[Dict[str, str]]) -> None:
    """Function to display all carparks at a given location"""
    print("Option 8: Display All Carparks at Given Location")

    # Get location input from user
    location = input("Please enter the location to search for: ")
    location = location.upper()

    # Filter carpark data by address
    carparks_at_location = [
        cp for cp in all_cp_info if location in cp["Address"]]

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
        address = cp["Address"].strip("\"")

        print("{:10} {:>10} {:>14} {:10.1f}   {}".format(
            num, total, available, percentage, address))

    # Display length
    print("Total number: {}".format(len(carparks_at_location)))


def option_9(_: List[Dict[str, str]], all_cp_info: List[Dict[str, str]]) -> None:
    """Function to display carparks with the most parking lots"""
    print("Option 9: Display carpark with the most parking lots")

    # Get the highest carpark
    highest_cp = all_cp_info[0]
    for cp in all_cp_info:
        if int(cp["Total Lots"]) > int(highest_cp["Total Lots"]):
            highest_cp = cp

    # Get the carpark information
    num = highest_cp["Carpark Number"]
    cp_type = highest_cp["Carpark Type"]
    parking_type = highest_cp["Type of Parking System"]
    total = highest_cp["Total Lots"]
    available = highest_cp["Lots Available"]
    percentage = highest_cp["Percentage"]
    address = highest_cp["Address"]

    # Display "No Address Found" if address is empty
    if address == "":
        address = "No Address Found"

    # Remove quotations from address
    address = address.strip("\"")

    # Display carpark information
    print("Carpark Number: {}".format(num))
    print("Carpark Type: {}".format(cp_type))
    print("Type of Parking System: {}".format(parking_type))
    print("Total Lots : {}".format(total))
    print("Lots Available: {}".format(available))
    print("Percentage: {:.1f}%".format(percentage))
    print("Address: {}".format(address))


def option_10(_: List[Dict[str, str]], all_cp_info: List[Dict[str, str]], timestamp: str) -> None:
    """Function to create output file with sorted carpark info"""
    # Sort by available lots
    # Line taken from: https://stackoverflow.com/questions/72899/how-to-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary-in-python
    sorted_carpark = sorted(
        all_cp_info, key=lambda cp: int(cp["Lots Available"]))

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
    cp_info = get_carpark_information()
    all_cp_info = None
    timestamp = None

    # Mainloop
    while True:
        option = main_menu()  # Get option from user
        print()  # Padding

        # Quit if user inputs 0
        if option == 0:
            break

        # Check if option 3 has been ran for options 4..=7
        if option > 3 and all_cp_info is None:
            print("Please run option 3 first!")
            continue

        # Run specified option
        if option != 3 and option != 10:
            eval("option_{}({}, {})".format(option, cp_info, all_cp_info))
        elif option == 10:
            option_10(cp_info, all_cp_info, timestamp)
        else:
            timestamp, all_cp_info = option_3(cp_info, all_cp_info)
