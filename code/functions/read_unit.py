def read_unit(input_message="Select unit from your hand: "):
    """
    Reads unit and returns it in lowercase
    """
    unit = input(input_message)
    return unit.lower()
