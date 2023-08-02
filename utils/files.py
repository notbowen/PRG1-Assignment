# Name: Hu Bowen (S10255800B)
# Date: 1 Aug 2023
#
# files.py
# File to handle file I/O, in charge of parsing data in ./res

import os
from typing import List

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

def write_file(filename: str, content: str) -> None:
    """Function to write data into a specified filename in the ./res folder

    Args:
        filename (str): Name of the file to write to
        content (str): Content to write to the file
    """

    # Get absolute path to the file
    # WARN: Program must be started in directory containing main.py
    res_path = os.path.join(os.getcwd(), RESOURCE_PATH)
    file_path = os.path.join(res_path, filename)

    # Write content to the file
    with open(file_path, "w") as f:
        f.write(content)
