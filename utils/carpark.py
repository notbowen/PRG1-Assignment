# Name: Hu Bowen (S10255800B)
# Date: 1 Aug 2023
# Last Modified: 2 Aug 2023
#
# carpark.py
# In charge of giving properly formatted carpark information

from typing import Dict, List
from utils.files import load_file

# Global variables for caching
carpark_info = None
all_carpark_info = None
timestamp = None


def get_carpark_information() -> List[Dict[str, str]]:
    """Loads and caches the carpark information

    Returns:
        List[Dict[str, str]]: List of carpark information formatted accordingly
    """
    global carpark_info

    # Check if carpark info has been cached, and cache it if it hasn't
    if carpark_info is not None:
        return carpark_info

    carpark_info = load_file("carpark-information.csv")
    carpark_info = parse_carpark_information(carpark_info)

    # Return carpark information
    return carpark_info


def get_all_carpark_info() -> List[Dict[str, str]]:
    """Function to get all the carpark information,
    including availability and information.
    Caches the data for performance improvement.

    WARNING: This function will fail when called before calling load_all_carpark_info

    Args:
        filename (str): The filename to load carpark availability from

    Returns:
        List[Dict[str, str]]: All carpark information formatted accordingly
    """

    # Check if all cp info has been cached, if not crash the program
    if all_carpark_info is None:
        raise TypeError("Expected all_carpark_info to have a value, not None.")

    return all_carpark_info


def associate_carpark_info(available_cps: List[str]) -> List[Dict[str, str]]:
    """Function to load all carpark information based on filename,
    without caching

    Args:
        filename (str): The filename to load carpark availability from

    Returns:
        List[Dict[str, str]]: All carpark information formatted accordingly
    """

    # Make all_carpark_info global to overwrite
    global all_carpark_info, timestamp

    # Load carpark info into a structure of:
    # {carpark_name: [list_of_carpark_info]}
    cp_info = {}
    for cp in carpark_info:
        cp_info[cp["Carpark Number"]] = [
            cp["Carpark Type"],
            cp["Type of Parking System"],
            cp["Address"]
        ]

    # Load available carparks, and remove timestamp
    timestamp = available_cps.pop(0)
    available_cps = parse_carpark_information(available_cps)

    # Map all the available carparks into the loaded cp_info,
    # Leaves some values blank if no associated carpark is found
    for cp in available_cps:
        # Map type & address
        try:
            cp_data = cp_info[cp["Carpark Number"]]
            cp["Carpark Type"] = cp_data[0]
            cp["Type of Parking System"] = cp_data[1]
            cp["Address"] = cp_data[2]
        except KeyError:
            cp["Carpark Type"] = ""
            cp["Type of Parking System"] = ""
            cp["Address"] = ""

        # Map percentage
        available_lots = int(cp["Lots Available"])
        total_lots = int(cp["Total Lots"])

        if total_lots != 0:
            percentage = (available_lots / total_lots) * 100
        else:
            percentage = 0.0

        cp["Percentage"] = percentage

    all_carpark_info = available_cps
    return all_carpark_info


def parse_carpark_information(data: List[str]) -> List[Dict[str, str]]:
    """Function to parse carpark information, parses into a list of
    dictionaries with the key as the header, and the value as the 
    respective values

    Args:
        data (List[str]): Carpark information in a list of strings

    Returns:
        List[Dict[str, str]]: List of dictionaries containing the parsed information
    """
    # Initialise return variable
    carpark_information = []

    # Get CSV headers
    headers = data.pop(0)

    # Loop through data, format and append
    for info in data:
        carpark_dict = {k: v for k, v in zip(
            headers.split(','), info.split(','))}
        carpark_information.append(carpark_dict)

    # Return the list of dicts
    return carpark_information


def get_timestamp() -> str:
    """Function to return the timestamp read from the .csv file
    WARNING: Run load_all_carpark_info() before running this

    Returns:
        str: The timestamp
    """

    if timestamp is None:
        raise TypeError("Expected timestamp to have a value, got None.")

    return timestamp
