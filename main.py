from code.warchest import Warchest
import pandas as pd
import datetime

if __name__ == "__main__":
    old_players = pd.read_csv('players_db.csv')
    old_players_sorted = old_players.sort_values('first_game', ascending=False)
    old_players = old_players.to_dict()
    print('Before starting the game you can see all the players that have already played warchest, their wins and when did they do it.')
    print(old_players_sorted)
    print('Welcome to the Warchest game, first of all you are going to enter the names of the 2 players')
    name_player_1 = input('Enter player 1 name: ')
    name_player_2 = input('Enter player 2 name: ')
    game = Warchest(name_player_1, name_player_2)
    winner = game.play()
    max_index = max(old_players['name'].keys())
    if name_player_1 not in old_players['name'].values():
        max_index += 1
        old_players['name'][max_index] = name_player_1
        old_players['games_played'][max_index] = 0
        old_players['wins'][max_index] = 0
        old_players['first_game'][max_index] = datetime.datetime.now()
    
    if name_player_2 not in old_players['name'].values():
        max_index += 1
        old_players['name'][max_index] = name_player_2
        old_players['games_played'][max_index] = 0
        old_players['wins'][max_index] = 0
        old_players['first_game'][max_index] = datetime.datetime.now()

    for index, name in old_players['name'].items():
        if name == name_player_1:
            index_player_1 = index
        if name == name_player_2:
            index_player_2 = index

    if winner == name_player_1:
        old_players['wins'][index_player_1] += 1
    else:
        old_players['wins'][index_player_2] += 1

    old_players['games_played'][index_player_1] += 1
    old_players['games_played'][index_player_2] += 1

    old_players = pd.DataFrame(old_players)
    old_players.to_csv('players_db.csv', index=False)