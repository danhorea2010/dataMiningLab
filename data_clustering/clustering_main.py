from clustering_wrapper import ClusteringWrapper
from clustering_functions import k_means_clustering, chebyshevDistance

from functools import partial

# For testing only
def main() -> None:
    move1 = (2,1)
    move2 = (5,5)

    # Use k-means with 3 clusters
    k_means_clustering_partial = partial(k_means_clustering, 3)

    clustering = ClusteringWrapper(
        ClusteringFunction=k_means_clustering_partial,
        ChessDistance=chebyshevDistance
    )

    
    print(clustering.get_distance(move1, move2))
    print(clustering.get_clusters([(1,1),(2,2),(3,3)]))

     

if __name__ == "__main__":
    main()