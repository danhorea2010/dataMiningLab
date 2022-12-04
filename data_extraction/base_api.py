from abc import ABC, abstractmethod
from typing import List

from data_extraction.extract_gameplayer import GamePlayerExtractor
from data_extraction.extract_moves import MovesExtractor
from data_extraction.extract_player import PlayerExtractor
from data_extraction.extract_verifier import AbstractVerifier, AlwaysOkVerifier

from models.game import Game, GamePlayer
from models.player import PlayerStats


class BaseAPI(ABC):
    def get_game(self, game_info, move_extractor: MovesExtractor, player_extractor: GamePlayerExtractor) -> Game:
        return Game(
            self.get_white_in_game(game_info, player_extractor),
            self.get_black_in_game(game_info, player_extractor),
            self.get_moves(game_info, move_extractor)
        )

    @classmethod
    @abstractmethod
    def get_moves(cls, game_info, extractor: MovesExtractor) -> List[str]:
        pass

    @classmethod
    @abstractmethod
    def get_games(cls, game_info, verifier: AbstractVerifier = AlwaysOkVerifier) -> List[Game]:
        pass

    @classmethod
    @abstractmethod
    def get_white_in_game(cls, game_info, extractor: GamePlayerExtractor) -> GamePlayer:
        pass

    @classmethod
    @abstractmethod
    def get_black_in_game(cls, game_info, extractor: GamePlayerExtractor) -> GamePlayer:
        pass
