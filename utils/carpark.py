# Name: Hu Bowen (S10255800B)
# Date: 1 Aug 2023
# Last Modified: 2 Aug 2023
#
# carpark.py
# In charge of giving properly formatted carpark information

import requests
import dotenv
import sys
import os

from typing import Dict, List
from utils.files import load_file


def get_carpark_information() -> List[Dict[str, str]]:
    """Loads and caches the carpark information

    Returns:
        List[Dict[str, str]]: List of carpark information formatted accordingly
    """
    global carpark_info

    carpark_info = load_file("carpark-information.csv")
    carpark_info = parse_carpark_information(carpark_info)

    # Return carpark information
    return carpark_info


def associate_carpark_info(
    available_cps: List[Dict[str, str]],
    carpark_info: List[Dict[str, str]],
    get_location: bool = False
) -> List[Dict[str, str]]:
    """Function to load all carpark information based on filename,
    without caching

    Args:
        available_cps (List[Dict[str, str]]): The carpark data formatted accordingly
        carpark_info (List[Dict[str, str]]): The carpark info formatted accordingly
        get_location (bool): Whether to associate location data with the info

    Returns:
        List[Dict[str, str]]: All carpark information formatted accordingly
    """

    # Make all_carpark_info global to overwrite
    global all_carpark_info

    # Load carpark info into a structure of:
    # {carpark_name: [list_of_carpark_info]}
    cp_info = {}
    for cp in carpark_info:
        cp_info[cp["Carpark Number"]] = [
            cp["Carpark Type"],
            cp["Type of Parking System"],
            cp["Address"]
        ]

    # Load location information if required
    if get_location:
        locations = get_carpark_locations()
        for carpark_no, location in locations.items():
            # Tries to load information
            try:
                cp_info[carpark_no].append(location)
            except KeyError:
                pass

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

        # Map location
        if get_location and cp_data:
            try:
                cp["Location"] = cp_data[3]
            except IndexError:
                cp["Location"] = None  # None if carpark location isn't found

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
            headers.split(',', 3), info.split(',', 3))}
        carpark_information.append(carpark_dict)

    # Return the list of dicts
    return carpark_information


def set_timestamp(tstamp: str) -> None:
    """Function to set the timestamp

    Args:
        tstamp (str): The value of the timestamp
    """
    global timestamp
    timestamp = tstamp


def get_timestamp() -> str:
    """Function to return the timestamp read from the .csv file
    WARNING: Run load_all_carpark_info() before running this

    Returns:
        str: The timestamp
    """

    if timestamp is None:
        raise TypeError("Expected timestamp to have a value, got None.")

    return timestamp


def get_carpark_locations() -> Dict[str, str]:
    """Gets the realtime carpark location datafrom LTA API

    Returns:
        Dict[str, str]: The realtime carpark location
    """
    # Loads the neccessary API keys
    dotenv.load_dotenv()
    api_key = os.getenv("API_KEY")

    # Make the request to LTA API
    r = requests.get("http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2",
                     headers={"AccountKey": api_key})

    # Tries to load realtime data, crashes when data cannot be retrieved
    try:
        realtime_data = r.json()["value"]
    except Exception as e:
        print("Couldn't load realtime LTA data!")
        print("Error: {}".format(e))
        sys.exit(1)

    # Formats data
    formatted_data = {}
    for cp in realtime_data:
        # Skip if not HDB Carpark
        if cp["Agency"] != "HDB":
            continue

        # Map location to carpark number
        formatted_data[cp["CarParkID"]] = cp["Location"]

    return formatted_data


def get_realtime_info() -> List[Dict[str, str]] | None:
    """Gets the realtime parking data from gov API

    Returns:
        List[Dict[str, str]]: The carpark data formatted
    """

    # Get data from API
    try:
        r = requests.get(
        "https://api.data.gov.sg/v1/transport/carpark-availability")
    except Exception as e:
        print("Error while fetching data!")
        print("Error: " + str(e))
        return None

    # Parse data & Handle failed request
    try:    
        data = r.json()["items"][0]["carpark_data"]
    except Exception as e:
        print("Error while getting realtime info!")
        print("Error: " + str(e))
        return None

    formatted_data = []

    for cp in data:
        cp_info = {}
        cp_info["Carpark Number"] = cp["carpark_number"]
        cp_info["Total Lots"] = cp["carpark_info"][0]["total_lots"]
        cp_info["Lots Available"] = cp["carpark_info"][0]["lots_available"]
        formatted_data.append(cp_info)

    return formatted_data
