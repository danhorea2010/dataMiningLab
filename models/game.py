from typing import List


class GamePlayer:
    def __init__(self, rating, result):
        self.rating = rating
        self.result = result


class Game:
    black: GamePlayer
    white: GamePlayer
    move_list: List[str]

    def __init__(
            self,
            white: GamePlayer,
            black: GamePlayer,
            moves: List[str]
    ) -> None:
        self.move_list = moves
        self.white = white
        self.black = black
