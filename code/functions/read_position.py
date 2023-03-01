def read_position(input_message="Select position to place: "):
    from_letter_to_row = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    pos = input(f'{input_message}(row, col) ')
    pos = pos.split(",")
    pos = (int(pos[1]), from_letter_to_row[pos[0].upper()])
    return pos
