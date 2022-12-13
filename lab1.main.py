import pickle

from requests import JSONDecodeError

from APIs.chesscom import ChessAPI
from models.game import Game, GamePlayer
from models.player import PlayerStats


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
    # players = ["Rahau", "samuelplayer"]
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


def main():
    data3 = get_data(100, 1201, 1400)
    with open('data/test.pickle', 'wb') as file:
        pickle.dump(data3, file)
        print("done")

if __name__ == "__main__":
    main()
