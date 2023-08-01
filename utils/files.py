# Name: Hu Bowen (S10255800B)
# Date: 1 Aug 2023
#
# files.py
# File to handle file I/O, in charge of parsing data in ./res

import os
from typing import Dict, List

RESOURCE_PATH = "./res"


def load_file(filename: str) -> List[str] | None:
    """Tries to read a file and returns its content in a list of strings
    WARNING: Returns None if file is not found, never throws an exception

    Args:
        filename (str): Name of the file to read

    Returns:
        List[str] | None: Content of the file, None if file is not found
    """

    # Get absolute path to the file
    # WARN: Program must be started in directory containing main.py
    res_path = os.path.join(os.getcwd(), RESOURCE_PATH)
    file_path = os.path.join(res_path, filename)

    with open(file_path) as f:
        data = f.read()

    return data.splitlines()

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
