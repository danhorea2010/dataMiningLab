from abc import abstractmethod, ABC
from typing import Tuple
import re


class ChessMoveConverter(ABC): 
    @classmethod
    @abstractmethod
    def chess_move_to_coord(move:str) -> Tuple[int,int]:
        pass

    @classmethod
    @abstractmethod
    def coord_to_chess_move(coord: Tuple[int, int]) -> str:
        pass


class ChessConverter(ChessMoveConverter):
    def chess_move_to_coord(move:str) -> Tuple[int,int]:
        """Converts a chess move in the format "QE3" or "E3" to a coordinate tuple (x, y)."""
        # Does not work for castleing or "+" moves
        
        #print("OLD MOVE: " + move)

        if 'x' in move: 
            return (2,1,1)

        move = re.sub(r'[x\+#]', '', move)
        move = move.upper()

        if len(move) > 3: 
            return (2,1,1)

        #print("NEW MOVE: " + move)
        # Does not currently handle castleing 
        if "O" in move:
            return (5, 0,0)

        if len(move) == 2:
            # The move is in the format "E3" (pawn moves to E3)
            # Assume that the piece is a pawn (index 0)
            index = 0
        
            # Extract the square from the move
            square = move
        else:
            # The move is in the format "QE3" (queen moves to E3)
            # Extract the piece and the destination square from the move
            piece = move[0]
            square = move[1:]

            # Convert the piece to an index (0 for pawn, 1 for knight, etc.)
            pieces = "PNBRQK"
            index = pieces.index(piece)

        # Convert the square to a coordinate
        x = ord(square[0]) - ord("A")
        y = int(square[1]) - 1

        return (index,x, y)



    def coord_to_chess_move(coord: Tuple[int, int]) -> str:
        """Converts a coordinate tuple (x, y) to a chess move in the format "QE3" or "E3"."""
        # Does not work for castleing or "+" moves
        # Extract the index and coordinates from the tuple
        index, x, y = coord
        if index == 0:
            # The piece is a pawn (index 0)
            # Return the move in the format "E3" (pawn moves to E3)
            column = chr(x + ord("A"))
            row = str(y + 1)
            square = column + row
            return square
        else:
            # The piece is not a pawn
            # Convert the index to a piece (0 for pawn, 1 for knight, etc.)
            pieces = "PNBRQK"
            piece = pieces[index]
            # Convert the coordinates to a square
            column = chr(x + ord("A"))
            row = str(y + 1)
            square = column + row
        
            return piece + square



