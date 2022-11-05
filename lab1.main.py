import requests

class GamePlayer:
    def __init__(self,rating,result):
        self.rating = rating
        self.result = result

class Game:
    def __init__(self) -> None:
        # TODO: extract move list from pgn
        self.move_list = []

    def extract_game(response):
        game = Game()

        game.whitePlayer = GamePlayer(response["white"]["rating"],response["white"]["result"])
        game.blackPlayer = GamePlayer(response["black"]["rating"],response["black"]["result"])

        return game

class PlayerStats:
    def __init__(self, rapid_rating: int, bullet_rating:int, blitz_rating:int):
        self.rapid_rating = rapid_rating
        self.bullet_rating = bullet_rating
        self.blitz_rating = blitz_rating
    
    def get_or_default(response, to_get) -> int:
        try:
            for sub in to_get:
                response = response[sub]
            return response
        except KeyError:
            return 0

    def extract_stats( response):
        player = PlayerStats(
            PlayerStats.get_or_default(response, ["chess_rapid", "last", "rating"]),
            PlayerStats.get_or_default(response, ["chess_blitz", "last", "rating"]),
            PlayerStats.get_or_default(response, ["chess_bullet","last","rating"])
        )

        return player

class ChessAPI:
    def __init__(self):
        self.base_endpoint = "https://api.chess.com/pub/"
        self.player_endpoint = "player/"
        self.stats_endpoint = "stats/"
        self.games_endpoint = "games/"
        self.archives_endpoint = "archives/"

    def get_player(self,player_name):
        return requests.get(f"{self.base_endpoint}{self.player_endpoint}/{player_name}").json()

    def get_stats(self, player_name :str) -> PlayerStats:
        response = requests.get(f"{self.base_endpoint}{self.player_endpoint}{player_name}/{self.stats_endpoint}").json()
        return PlayerStats.extract_stats(response)

    def get_monthly_games_list(self, player_name:str):
        return requests.get(f"{self.base_endpoint}{self.player_endpoint}{player_name}/{self.games_endpoint}{self.archives_endpoint}").json()["archives"]

    def get_monthly_games_data(self, player_name: str):
        game_list = self.get_monthly_games_list(player_name)
        game_data_list = []

        for url in game_list:
            game_list = self.get_data_from_game_url(url)
            game_data_list.extend(game_list)
        
        return game_data_list

    def get_data_from_game_url(self, url):
        response_list = requests.get(url).json()["games"]
        games_list = []

        for game in response_list:
            extracted_game = Game.extract_game(game)
            games_list.append(extracted_game)

        return games_list


def main():
    test = ChessAPI()
    x = test.get_monthly_games_data("Raugan") 
    
    for game in x:
        print(vars(game.whitePlayer))
        print(vars(game.blackPlayer))



if __name__ == "__main__" :
    main()