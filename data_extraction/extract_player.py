from abc import abstractmethod, ABC

from models.player import PlayerStats


class PlayerExtractor(ABC):
    @classmethod
    @abstractmethod
    def get_player(cls, game_info) -> PlayerStats:
        pass