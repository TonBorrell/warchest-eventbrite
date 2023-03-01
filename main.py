from code.warchest import Warchest

if __name__ == "__main__":
    print('Welcome to the Warchest game, first of all you are going to enter the names of the 2 players')
    name_player_1 = input('Enter player 1 name: ')
    name_player_2 = input('Enter player 2 name: ')
    game = Warchest(name_player_1, name_player_2)
    game.play()
