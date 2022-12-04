from dataclasses import dataclass
from clustering_functions import Clustering, Distance

@dataclass
class ClusteringWrapper:
    # Generic function definitions
    ClusteringClass: Clustering
    DistanceClass: Distance 

    def get_distance(self,first_move: tuple[(int,int)], second_move: tuple[(int,int)]) -> float:
        return self.DistanceClass.get_distance(first_move, second_move)

    def get_clusters(self, moves: list[tuple[int,int]], number_of_clusters: int) -> list[float]:
        return self.ClusteringClass.cluster(moves, number_of_clusters) 


