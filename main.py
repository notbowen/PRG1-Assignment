# Name: Hu Bowen (S10255800B)
# Date: 1 Aug 2023
# Last Modified: 2 Aug 2023
#
# main.py
# In charge of getting the user input to switch between basic and advanced mode
# Before running the respective scripts

from utils.input import validate_input_str
from basic import main as basic_main
from advanced import main as advanced_main

title = """
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
    print("by typing B(asic) or A(dvanced), to choose basic or advanced respectively.")

    choice = validate_input_str("> ", "B", "A", ignore_case=True)

    if choice.upper() == "B":
        basic_main()
    else:
        advanced_main()

if __name__ == "__main__":
    main()