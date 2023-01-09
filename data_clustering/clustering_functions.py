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
    def get_distance(self, first_move: Tuple[float,float], second_move: Tuple[float,float]) -> float:
        pass

class Clustering(ABC):
    @classmethod
    @abstractmethod
    def cluster(self, move_list: List[Tuple[float,float]], number_of_clusters: int):
        pass

class ManhattanDistance(Distance):
     def get_distance(self, first_move: Tuple[float,float], second_move: Tuple[float,float]) -> float:
        diff_rank = abs(first_move[0] - second_move[0])
        diff_file = abs(first_move[1] - second_move[1])
        return (diff_rank+ diff_file)

class EuclidianDistance(Distance):
    def get_distance(self, first_move: Tuple[float,float], second_move: Tuple[float,float]) -> float:
        """Computes the Euclidean distance between two points (x, y)."""
        x1, y1 = first_move
        x2, y2 = second_move
        return math.sqrt((x1 - x2) ** 2 + (y1-y2) ** 2)

   
class KMeansClustering(Clustering):

    def __init__(self, distance:Distance) -> None:
        self.Distance = distance

    def cluster(self, moves: List[Tuple[float,float]], number_of_clusters: int):
        max_iterations = 1000
        # Initialize the first centroid randomly
        centroids = [random.choice(moves)]
        # Initialize empty clusters 
        clusters = [[] for _ in range(number_of_clusters)]

        # Select the remaining centroids using the kmeans++ method
        for i in range(1, number_of_clusters):
            # Compute the sum of squared distances to the nearest centroid
            squared_dists = []
            for move in moves:
                min_distance = float("inf")
                for centroid in centroids:
                    distance = self.Distance.get_distance(move, centroid) ** 2
                    if distance < min_distance:
                        min_distance = distance
                squared_dists.append(min_distance)

            # Select the next centroid with probability proportional to the squared distance
            total_squared_dists = sum(squared_dists)
            prob = [dist / total_squared_dists for dist in squared_dists]
            centroids.append(random.choices(moves, weights=prob)[0])

        # Iterate until convergence or until max_iterations is reached
        clusters = [[] for i in range(number_of_clusters)]
        for i in range(max_iterations):
            #print("ITERATION: " + str(i))
            # Assign each point to the closest centroid
            for move in moves:
                closest_centroid = None
                min_distance = float("inf")
                for centroid in centroids:
                    distance = self.Distance.get_distance(move, centroid)
                    if distance < min_distance:
                        closest_centroid = centroid
                        min_distance = distance
                clusters[centroids.index(closest_centroid)].append(move)

            # Store the previous centroids to check for convergence
            prev_centroids = copy.deepcopy(centroids)

           # Re-compute the centroids as the mean of the points in the cluster
            for i in range(number_of_clusters):
                centroids[i] = Mean.mean(clusters[i])
        
            # Check for convergence
            # This might never happen and we might all be doomed
            if prev_centroids == centroids:
                break

        return [centroids, clusters]


class KNearestNeighborClustering(Clustering):

    def __init__(self, distance: Distance) -> None:
        self.Distance = distance

    def cluster(self, moves: List[Tuple[float, float]], number_of_centers: int):
        centroids = {}
        clusters = {}
        number_of_neighbors = round(len(moves) / number_of_centers)
        if not len(moves) == number_of_centers * number_of_neighbors:
            number_of_neighbors += 1
        centers = range(number_of_centers)
        moves_copy = moves.copy()
        for center in centers:
            random_index = random.randrange(len(moves_copy))
            centroids[center] = moves_copy[random_index]
            moves_copy.remove(centroids[center])
            clusters[center] = [centroids[center]]
        number_of_iterations = range(number_of_neighbors - 1)
        for iteration in number_of_iterations:
            for [number, centroid] in centroids.items():
                if len(moves_copy) <= 0:
                    continue
                min_dist_move = moves_copy[0]
                min_dist_move_dist = self.Distance.get_distance(moves_copy[0], centroid)
                for move in moves_copy:
                    move_dist = self.Distance.get_distance(move, centroid)
                    if min_dist_move_dist > move_dist:
                        min_dist_move_dist = move_dist
                        min_dist_move = move
                moves_copy.remove(min_dist_move)
                clusters[number].append(min_dist_move)
                newX = 0
                newY = 0
                for cluster_part in clusters[number]:
                    newX += cluster_part[0]
                    newY += cluster_part[1]
                newCenter = [round(newX / len(clusters[number]), 2), round(newY / len(clusters[number]), 2)]
                centroids[number] = newCenter
        return [centroids, clusters]
