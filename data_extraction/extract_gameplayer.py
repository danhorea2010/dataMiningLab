from abc import abstractmethod, ABC

from models.game import GamePlayer


class GamePlayerExtractor(ABC):
    @classmethod
    @abstractmethod
    def get_game_player(self, game_info) -> GamePlayer:
        pass