from typing import Callable
from abc import ABC, abstractclassmethod

# Function that receives a list of chess moves and returns a list of centroids
ClusteringStategyFunction = Callable[[list[tuple[int, int]]], list[float]]

# Function that receives 2 chess moves and returns their difference
ChessDistanceFunction = Callable[[tuple[int,int], tuple[int,int]], float]

class Distance(ABC):
    @abstractclassmethod
    def get_distance(first_move: tuple[int,int], second_move: tuple[int,int]) -> float:
        pass

class Clustering(ABC):
    @abstractclassmethod
    def cluster(move_list: list[tuple[int,int]], number_of_clusters: int) -> list[float]:
        pass

class ChebyshevDistance(Distance):
    def get_distance(first_move: tuple[int,int], second_move: tuple[int,int]) -> float:
        diff_rank = abs(first_move[0] - second_move[0])
        diff_file = abs(first_move[1] - second_move[1])
        return max(diff_rank, diff_file)

class ManhattanDistance(Distance):
     def get_distance(first_move: tuple[int,int], second_move: tuple[int,int]) -> float:
        diff_rank = abs(first_move[0] - second_move[0])
        diff_file = abs(first_move[1] - second_move[1])
        return (diff_rank+ diff_file)

       
class KMeansClustering(Clustering):
    def cluster(move_list: list[tuple[int,int]], number_of_clusters: int) -> list[float]:
        return number_of_clusters * move_list
