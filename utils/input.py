from typing import List

INVALID_PROMPT = "Invalid input! Please enter again!"


def validate_str(
    prompt: str,
    *values_to_accept: str,
    ignore_case: bool = False,
    invalid_prompt: str = INVALID_PROMPT
) -> str:
    """Function to validate a user's string input,
    and returns the value only if it matches the values to accept.

    WARNING: The returned value will not be capitalized,
    remember to format it accordingly.

    Examples:
        ```py
        # Only valid if the user inputs `A` or `B`, not `a` or `b`
        validate_str("Input A or B: ", "A", "B", True)

        # Valid if user inputs a, b, A or B
        validate_str("Input A or B: ", "A", "B")
        ```

    Args:
        prompt (str): The user prompt
        values_to_accept (str): The values to be accepted, seperated by commas
        ignore_case (bool): Toggles the case sensitivity of the validation
        invalid_prompt (str): The output to the user if their input is invalid

    Returns:
        str: A valid string that is one of the values of `values_to_accept`
    """

    # Makes list lowercase if ignore_case is set
    if ignore_case:
        values_to_accept = [x.lower() for x in values_to_accept]

    while True:
        # Get input from user
        user_input = input(prompt)

        # Lower the input if we want to ignore case, to match the list
        if ignore_case:
            user_input = user_input.lower()

        # Check if user input is valid
        if user_input in values_to_accept:
            break

        # Alert user that their input is invalid
        print(invalid_prompt)

    # Data is valid, return
    return user_input


def validate_num(
        prompt: str,
        values_to_accept: List[int | float] | range | str,
        invalid_prompt: str = INVALID_PROMPT
) -> int | float:
    """Validates user input based on the value.

    Examples:
        ```py
        # Accepts any integer
        validate_num("Enter an int: ", "int")

        # Accepts any integer/float between 0 and 4 (inclusive)
        validate_num("Enter a value between 0 and 4: ", range(5))
        ```

    Args:
        prompt (str): The prompt to prompt the user

        values_to_accept (List[int  |  float] | range | str): Values to accept. Can be a
        list of floats or integers, range, or "int" or "float"

        invalid_prompt (str, optional): The prompt to show the user when their input is
        invalid. Defaults to "Invalid input! Please enter again.".

    Returns:
        int | float: The valid integer or float
    """

    while True:
        user_input = input(prompt)

        # Integer validation
        if user_input.isdigit():
            user_input = int(user_input)
            if values_to_accept == "int":
                return user_input

        # Float validation
        elif user_input.replace('.', '', 1).isdigit():
            user_input = float(user_input)
            if values_to_accept == "float":
                return user_input

        # Check if user input is in valid range
        if user_input in values_to_accept:
            return user_input

        # Check if float is within the specified range
        if type(values_to_accept) == range:
            if values_to_accept.start <= user_input <= (values_to_accept.stop - 1):
                return user_input

        print(invalid_prompt)
