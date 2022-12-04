from abc import abstractmethod, ABC

from models.game import Game


class AbstractVerifier(ABC):
    @classmethod
    @abstractmethod
    def is_game_accepted(cls, game: Game) -> bool:
        pass


class AlwaysOkVerifier(AbstractVerifier):

    @classmethod
    def is_game_accepted(cls, game: Game) -> bool:
        return True