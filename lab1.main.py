from typing import List

import matplotlib.pyplot as plt
import pandas as pd
from requests import JSONDecodeError

from APIs.chesscom import ChessAPI
from data_clustering.clustering_convertions import ChessConverter
from models.game import Game, GamePlayer

# k-means with 3/4/5 and clustering with 5

def get_games_for_player(player: str):
    return ChessAPI().get_games({"player_name": player})


def player_is_between_ratings(player: GamePlayer, rating1: int, rating2: int):
    return rating1 <= player.rating <= rating2


def black_is_between_ratings(game: Game, rating1: int, rating2: int):
    return player_is_between_ratings(game.black, rating1, rating2)


def white_is_between_ratings(game: Game, rating1: int, rating2: int):
    return player_is_between_ratings(game.white, rating1, rating2)


def get_data(number_of_game: int, min_rating: int, max_rating: int):
    players = ["Raugan"]
    players = ["Rahau", "samuelplayer"]
    processedPlayers = []
    games = []
    test = ChessAPI()
    finalgames = []
    intermediategames = []
    while len(players) > 0 and len(finalgames)< number_of_game:
        player = players.pop()
        try:
            games = test.get_games({"player_name": player})
        except (KeyError, JSONDecodeError) as e:
            print(e)
            games = []
        if len(games) == 0 and len(intermediategames) > 0:
            games = intermediategames
            intermediategames = []
        for game in games:
            if black_is_between_ratings(game, min_rating, max_rating) \
                    and white_is_between_ratings(game, min_rating, max_rating):
                if game.white.name not in processedPlayers and game.black.name not in processedPlayers:
                    finalgames.append(game)
                if game.white.name not in processedPlayers and game.white.name not in players:
                    players.append(game.white.name)
                    processedPlayers.append(player)
                if game.black.name not in processedPlayers and game.black.name not in players:
                    players.append(game.black.name)
                    processedPlayers.append(player)
        processedPlayers.append(player)
        print(len(finalgames))
    return finalgames


def print_game(game: Game):
    print(game.move_list)
    print(game.white.name)
    print(game.white.rating)
    print(game.black.name)
    print(game.black.rating)


# def main():
#     data1000_1200 = get_data(100, 1000, 1200)
#     with open('data/data1000_1200.pickle', 'wb') as file:
#         pickle.dump(data1000_1200, file)
#         print("done")


# def main():
#     data1200_1400 = get_data(100, 1200, 1400)
#     with open('data/data1200_1400.pickle', 'wb') as file:
#        pickle.dump(data1200_1400, file)
#        print("done")

# def main():
#     data1400_1600 = get_data(50, 1400, 1600)
#     with open('data/data1400_1600.pickle', 'wb') as file:
#         pickle.dump(data1400_1600, file)
#         print("done")

# def main():
#     data1600_1800 = get_data(100, 1600, 1800)
#     with open('data/data1600_1800.pickle', 'wb') as file:
#         pickle.dump(data1600_1800, file)
#         print("done")

def read_from_pickle(path):
    return pd.read_pickle(path)

def calculate_height(moves:List[str]) -> float:
    height = 0
    for move in moves:
        if move[0].islower():
            height+=1
        else:
            if move[0] == "N":
                height += 1/15
            elif  move[0] == "Q":
                height += 1/5
            elif  move[0] == "R":
                height += 1/10
            elif  move[0] == "B":
                height += 1/15
            elif  move[0] == "K":
                height += 1/3
            elif  move == "O-O":
                height += 1/3 + 1/10
            elif  move == "O-O-O":
                height += 1/3 + 1/10
            else:
                print(move, "da")
                exit()
    return round(height, 2)

def show(filename:str):
    game_moves = []
    for game in read_from_pickle(filename):
        game_moves.append(game.move_list)
    number_of_moves = 5

    relevantData = []
    stats = []
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    coordsx = []
    coordsy = []
    i = 0
    indexes = range(2 * number_of_moves)
    for moves in game_moves:
        if len(moves) < 2 * number_of_moves:
            continue
        white = []
        black = []
        for move_index in indexes:
            if move_index % 2 == 0:
                white.append(moves[move_index])
            else:
                black.append(moves[move_index])
        whiteHeight = calculate_height(white)
        blackHeight = calculate_height(black)
        relevantData.append([whiteHeight, blackHeight, white, black])
        coordsx.append(whiteHeight)
        coordsy.append(blackHeight)
    plt.scatter(coordsx, coordsy)
    plt.show()
    plt.clf()

def main():

    game_moves = []
    for game in read_from_pickle('data/data1000_1200.pickle'):

        game_moves.append(game.move_list)
    #
    # for game in read_from_pickle('data/data1200_1400.pickle'):
    #     game_moves.append(game.move_list)

    # for game in read_from_pickle('data/data1400_1600.pickle'):
    #     game_moves.append(game.move_list)

    # for game in read_from_pickle('data/data1600_1800.pickle'):
    #     game_moves.append(game.move_list)

    # Number of clusters
    k = 3
    converter = ChessConverter()
    filename = 'data/data1000_1200.pickle'
    show(filename)
    filename = 'data/data1200_1400.pickle'
    show(filename)
    filename = 'data/data1400_1600.pickle'
    show(filename)
    filename = 'data/data1600_1800.pickle'
    show(filename)

if __name__ == "__main__":
    main()