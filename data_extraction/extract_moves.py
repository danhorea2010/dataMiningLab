from abc import abstractmethod, ABC
from typing import List


class MovesExtractor(ABC):
    @classmethod
    @abstractmethod
    def get_moves(cls, game_info) -> List[str]:
        pass
