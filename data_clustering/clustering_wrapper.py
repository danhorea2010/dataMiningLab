from dataclasses import dataclass
from clustering_functions import ClusteringStategyFunction, ChessDistanceFunction

@dataclass
class ClusteringWrapper:
    # Generic function definitions
    ClusteringFunction: ClusteringStategyFunction
    ChessDistance: ChessDistanceFunction

    def get_distance(self,first_move: tuple[(int,int)], second_move: tuple[(int,int)]) -> float:
        return self.ChessDistance(first_move, second_move)

    def get_clusters(self, moves: list[tuple[int,int]]) -> list[float]:
        return self.ClusteringFunction(moves) 
