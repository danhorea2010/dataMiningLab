import re
from typing import List

import requests

from data_extraction.base_api import BaseAPI
from data_extraction.extract_gameplayer import GamePlayerExtractor
from data_extraction.extract_moves import MovesExtractor
from data_extraction.extract_verifier import AbstractVerifier, AlwaysOkVerifier
from models.game import GamePlayer, Game


def get_or_default(response, to_get) -> int:
    try:
        for sub in to_get:
            response = response[sub]
        return response
    except KeyError:
        return 0


class ChessComPlayerExtractor(GamePlayerExtractor):
    def get_game_player(self, game_info) -> GamePlayer:
        return GamePlayer(game_info["rating"], game_info["result"])


class ChessComPlayerMovesExtractor(MovesExtractor):
    def get_moves(self, game_info) -> List[str]:
        movesInPGNFormat = game_info["pgn"].split("\n")[-2]
        # split the moves string
        movesInNormalFormat = list(map(lambda move: re.sub("{.*", "", move), movesInPGNFormat.split("} ")))
        # remove the final score
        movesInNormalFormat.pop()
        # remove the remaning junk from moves
        move_list = list(map(lambda move: re.sub("\d+\.(\.\.)?", "", move).strip(), movesInNormalFormat))

        return move_list


class ChessAPI(BaseAPI):
    archives_endpoint: str
    games_endpoint: str
    stats_endpoint: str
    player_endpoint: str
    base_endpoint: str

    def __init__(self):
        self.base_endpoint = "https://api.chess.com/pub/"
        self.player_endpoint = "player/"
        self.stats_endpoint = "stats/"
        self.games_endpoint = "games/"
        self.archives_endpoint = "archives/"
        self.move_extractor = ChessComPlayerMovesExtractor()
        self.player_extractor = ChessComPlayerExtractor()

    def get_moves(self, game_info, extractor: MovesExtractor) -> List[str]:
        return extractor.get_moves(game_info)

    def get_games(self, game_info, verifier: AbstractVerifier = AlwaysOkVerifier) -> List[Game]:
        player_name = game_info["player_name"]
        results = []
        raw_game_urls = requests.get(
            f"{self.base_endpoint}{self.player_endpoint}{player_name}/{self.games_endpoint}{self.archives_endpoint}").json()["archives"]
        for raw_game_url in raw_game_urls:
            raw_games = requests.get(raw_game_url).json()["games"]
            for raw_game in raw_games:
                game = self.get_game(raw_game, self.move_extractor, self.player_extractor)
                if verifier.is_game_accepted(game):
                    results.append(game)
        return results

    def get_white_in_game(self, game_info, extractor: GamePlayerExtractor) -> GamePlayer:
        return extractor.get_game_player(game_info["white"])

    def get_black_in_game(self, game_info, extractor: GamePlayerExtractor) -> GamePlayer:
        return extractor.get_game_player(game_info["black"])
