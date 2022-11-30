from typing import Callable
# Function that receives a list of chess moves and returns a list of centroids
ClusteringStategyFunction = Callable[[list[tuple[int, int]]], list[float]]

# Function that receives 2 chess moves and returns their difference
ChessDistanceFunction = Callable[[tuple[int,int], tuple[int,int]], float]

def k_means_clustering(move_list: list[tuple[int,int]], number_of_clusters: int) -> list[float]:
    # Filler output 
    return number_of_clusters * move_list 

def chebyshevDistance(first_move: tuple[int,int], second_move: tuple[int,int]) -> float:
    diff_rank = abs(first_move[0] - second_move[0])
    diff_file = abs(first_move[1] - second_move[1])

    return max(diff_rank, diff_file)

def manhattanDistance(first_move: tuple[int,int], second_move: tuple[int,int]) -> float:
    diff_rank = abs(first_move[0] - second_move[0])
    diff_file = abs(first_move[1] - second_move[1])

    return (diff_file + diff_rank) 


