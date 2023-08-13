# Name: Hu Bowen (S10255800B)
# Date: 1 Aug 2023
# Last Modified: 2 Aug 2023
#
# main.py
# In charge of getting the user input to switch between normal and additional mode
# Before running the respective scripts

from S10255800_Assignment_Extra import main as additional_main
from S10255800_Assignment import main as normal_main
from utils.input import validate_input_str

title = r"""
  _____  _____   _____   __                    _                                  _   
 |  __ \|  __ \ / ____| /_ |     /\           (_)                                | |  
 | |__) | |__) | |  __   | |    /  \   ___ ___ _  __ _ _ __  _ __ ___   ___ _ __ | |_ 
 |  ___/|  _  /| | |_ |  | |   / /\ \ / __/ __| |/ _` | '_ \| '_ ` _ \ / _ \ '_ \| __|
 | |    | | \ \| |__| |  | |  / ____ \\__ \__ \ | (_| | | | | | | | | |  __/ | | | |_ 
 |_|    |_|  \_\\_____|  |_| /_/    \_\___/___/_|\__, |_| |_|_| |_| |_|\___|_| |_|\__|
                                                  __/ |                               
                                                 |___/                                
"""


def main():
    print(title)
    print("=============================================")
    print("Hi, welcome to my PRG1 Assignment.")
    print("Please choose between basic or advanced mode,")
    print("by typing N(normal) or A(dditional), to choose basic or advanced respectively.")

    choice = validate_input_str("> ", "N", "A", ignore_case=True)

    if choice.upper() == "N":
        normal_main()
    else:
        additional_main()


if __name__ == "__main__":
    main()
