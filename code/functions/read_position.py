def read_position(input_message="Select position to place: "):
    pos = input(input_message)
    pos = pos.split(",")
    pos = (int(pos[0]), int(pos[1]))
    return pos
