from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from requests import JSONDecodeError

from APIs.chesscom import ChessAPI
from data_clustering.clustering_functions import EuclidianDistance, KMeansClustering, KNearestNeighborClustering
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

def get_relvent_data(filename:str, number_of_moves:int) -> List[Tuple[float, float]]:
    relevant_data = []
    for game in read_from_pickle(filename):
        list_of_moves = game.move_list
        if len(list_of_moves) < 2 * number_of_moves :
            continue
        white = []
        black = []
        index_of_moves = range(0, 2 * number_of_moves)
        for index in index_of_moves:
            if index % 2 == 0:
                white.append(list_of_moves[index])
            else:
                black.append(list_of_moves[index])
        whiteHeight = calculate_height(white)
        blackHeight = calculate_height(black)
        relevant_data.append([whiteHeight, blackHeight])
    return relevant_data

def show(relevantData:List[Tuple[float, float]], circles:List[Tuple[Tuple[float, float], int]]):
    stats = []
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    coordsx = []
    coordsy = []
    fig, ax = plt.subplots()
    for circle in circles:
        ax.add_patch(plt.Circle((circle[0][0], circle[0][1]), circle[1], color='r', fill=False))
    for moves in relevantData:
        coordsx.append(moves[0])
        coordsy.append(moves[1])
    plt.scatter(coordsx, coordsy)
    plt.show()
    plt.clf()

def show_plots(centroids, clusters, relevant_data):
    centers = []
    for [number, centroid] in centroids.items():
        distanceX = 0
        distanceY = 0
        for move in clusters[number]:
            tempDistX = abs(move[0] - centroid[0])
            tempDistY = abs(move[1] - centroid[1])
            if tempDistX > distanceX:
                distanceX = tempDistX
            if tempDistY > distanceY:
                distanceY = tempDistY
        centers.append([centroid, round(max(distanceX, distanceY), 2)])
    show(relevant_data, centers)
def show_plots2(centroids, clusters, relevant_data):
    centers = []
    number = 0
    for centroid in centroids:
        distanceX = 0
        distanceY = 0
        for move in clusters[number]:
            tempDistX = abs(move[0] - centroid[0])
            tempDistY = abs(move[1] - centroid[1])
            if tempDistX > distanceX:
                distanceX = tempDistX
            if tempDistY > distanceY:
                distanceY = tempDistY
        centers.append([centroid, round(max(distanceX, distanceY), 2)])
        number += 1
    show(relevant_data, centers)
def show_data(filename:str, number_of_moves:int):
    relevant_data = get_relvent_data(filename, number_of_moves)
    show(relevant_data, [])
    kmeans = KMeansClustering(EuclidianDistance())
    centroids1, clusters1 = kmeans.cluster(relevant_data, 5)
    show_plots2(centroids1, clusters1, relevant_data)

    knearest = KNearestNeighborClustering(EuclidianDistance())
    centroids2, clusters2 = knearest.cluster(relevant_data, 5)
    show_plots(centroids2, clusters2, relevant_data)
def main():
    show_data('data/data1000_1200.pickle', 5)
    show_data('data/data1200_1400.pickle', 5)
    show_data('data/data1400_1600.pickle', 5)
    show_data('data/data1600_1800.pickle', 5)


    #
    # for game in read_from_pickle('data/data1200_1400.pickle'):
    #     game_moves.append(game.move_list)

    # for game in read_from_pickle('data/data1400_1600.pickle'):
    #     game_moves.append(game.move_list)

    # for game in read_from_pickle('data/data1600_1800.pickle'):
    #     game_moves.append(game.move_list)

    # Number of clusters
    k = 3
    # converter = ChessConverter()
    # filename = 'data/data1000_1200.pickle'
    # show(filename)
    # filename = 'data/data1200_1400.pickle'
    # show(filename)
    # filename = 'data/data1400_1600.pickle'
    # show(filename)
    # filename = 'data/data1600_1800.pickle'
    # show(filename)

if __name__ == "__main__":
    main()