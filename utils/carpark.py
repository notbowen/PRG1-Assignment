from typing import Dict, List


def get_cp_percentage(carpark_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Caches the carpark availability percentage into a specified cache variable

    Args:
        carpark_data (Dict[str, str]): The carpark data formatted as a list of dicts

    Returns:
        List[Dict[str, str]]: A list of dicts containing the percentage data
    """

    # Initialise variable to return
    cps = []

    # Loop through data and append to cps
    for cp in carpark_data:
        try:
            cp["Percentage"] = int(cp["Lots Available"]) / \
                int(cp["Total Lots"])
        except ZeroDivisionError:
            cp["Percentage"] = 0.0

        # Convert percentage from 0.9 to 90%
        cp["Percentage"] *= 100
        cps.append(cp)

    return cps


def cache_cp_address(
        carpark_info: List[Dict[str, str]],
        carpark_cache: List[Dict[str, str]]
    ) -> None:
    """Function to associate the carpark info with carpark availability
    by carpark number and write to a cache variable

    Args:
        carpark_info (List[Dict[str, str]]): Carpark information (with address)
        carpark_cache (List[Dict[str, str]]): Cached data to write to
    """

    # Increase performance by getting a key value pair of
    # carpark number and corresponding addresses
    cp_address = {}
    for cp in carpark_info:
        cp_address[cp["Carpark Number"]] = cp["Address"]

    # Loop through carpark availability and find corresponding address
    for cp in carpark_cache:
        try:
            cp["Address"] = cp_address[cp["Carpark Number"]]
        except KeyError:  # Leave empty addresses blank
            cp["Address"] = ""
