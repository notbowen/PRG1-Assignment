from typing import List

def validate_str(
        prompt: str,
        *values_to_accept: str,
        ignore_case: bool = False,
        invalid_prompt: str = "Invalid input! Please enter again."
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
