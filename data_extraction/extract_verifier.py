from abc import abstractmethod, ABC

from models.game import Game


class AbstractVerifier(ABC):
    @classmethod
    @abstractmethod
    def is_game_accepted(self, game: Game) -> bool:
        pass


class AlwaysOkVerifier(AbstractVerifier):
    def is_game_accepted(self, game: Game) -> bool:
        return True
