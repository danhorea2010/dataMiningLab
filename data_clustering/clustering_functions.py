from typing import Callable, Tuple, List
from abc import abstractmethod, ABC
import math
import random
import copy

from data_clustering.clustering_convertions import ChessConverter
from data_clustering.mean import Mean

class Distance(ABC):
    @classmethod
    @abstractmethod
    def get_distance(self, first_move: Tuple[int,int], second_move: Tuple[int, int]) -> float:
        pass

class Clustering(ABC):
    @classmethod
    @abstractmethod
    def cluster(self, move_list: List[Tuple[int, int]], number_of_clusters: int) -> List[float]:
        pass

class ChebyshevDistance(Distance):
    def get_distance(first_move: Tuple[int, int], second_move: Tuple[int, int]) -> float:
        diff_rank = abs(first_move[0] - second_move[0])
        diff_file = abs(first_move[1] - second_move[1])
        return max(diff_rank, diff_file)

class ManhattanDistance(Distance):
     def get_distance(first_move: Tuple[int,int], second_move: Tuple[int,int]) -> float:
        diff_rank = abs(first_move[0] - second_move[0])
        diff_file = abs(first_move[1] - second_move[1])
        return (diff_rank+ diff_file)

class EuclidianDistance(Distance):
    def get_distance(self, first_move: Tuple[int,int], second_move: Tuple[int,int]) -> float:
        """Computes the Euclidean distance between two points (x, y)."""
        #print("DISTANCE: " + str(first_move) + " . " + str(second_move))
        if len(first_move) == 2:
            # The piece is not specified in the coordinate tuple
            x1, y1 = first_move
            x2, y2 = second_move
            #return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            return (x1 - x2) ** 2 + (y1-y2) ** 2
        elif len(second_move) != 2:
            # The piece is specified in the coordinate tuple
            index_a, x1, y1 = first_move
            index_b, x2, y2 = second_move
            #return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (index_a - index_b) ** 2)
            return (x1 - x2) ** 2 + (y1-y2) ** 2 + (index_a - index_b) ** 2
        else:
            # Off case that maybe should not be an off case...
            _, x1, y1 = first_move
            x2, y2 = second_move
            #return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            return (x1-x2) ** 2 + (y1-y2) ** 2
   
class KMeansClustering(Clustering):

    def __init__(self, distance) -> None:
        self.Distance = distance

    def cluster(self, moves: List[Tuple[int,int]], number_of_clusters: int) -> List[float]:
        max_iterations = 10_000
        # Convert the moves to coordinates
        coords = [ChessConverter.chess_move_to_coord(move) for move in moves]

        # Initialize the first centroid randomly
        centroids = [random.choice(coords)]
        # Initialize empty clusters 
        clusters = [[] for _ in range(number_of_clusters)]

        # Select the remaining centroids using the kmeans++ method
        for i in range(1, number_of_clusters):
            # Compute the sum of squared distances to the nearest centroid
            squared_dists = []
            for coord in coords:
                min_distance = float("inf")
                for centroid in centroids:
                    distance = self.Distance.get_distance(coord, centroid) ** 2
                    if distance < min_distance:
                        min_distance = distance
                squared_dists.append(min_distance)

            # Select the next centroid with probability proportional to the squared distance
            total_squared_dists = sum(squared_dists)
            prob = [dist / total_squared_dists for dist in squared_dists]
            centroids.append(random.choices(coords, weights=prob)[0])

        # Iterate until convergence or until max_iterations is reached
        for i in range(max_iterations):
            #print("ITERATION: " + str(i))
            clusters = [[] for i in range(number_of_clusters)]
            # Assign each point to the closest centroid
            for coord in coords:
                closest_centroid = None
                min_distance = float("inf")
                for centroid in centroids:
                    distance = self.Distance.get_distance(coord, centroid)
                    if distance < min_distance:
                        closest_centroid = centroid
                        min_distance = distance
                clusters[centroids.index(closest_centroid)].append(coord)

            # Store the previous centroids to check for convergence
            prev_centroids = copy.deepcopy(centroids)

           # Re-compute the centroids as the mean of the points in the cluster
            for i in range(number_of_clusters):
                centroids[i] = Mean.mean(clusters[i])
        
            # Check for convergence
            # This might never happen and we might all be doomed
            if prev_centroids == centroids:
                break
    
        # Convert the clusters back to chess moves
        clusters_moves = [[ChessConverter.coord_to_chess_move(coord) for coord in cluster] for cluster in clusters]
    
        return clusters_moves


