from clustering_wrapper import ClusteringWrapper
from clustering_functions import ChebyshevDistance, KMeansClustering 
# For testing only
def main() -> None:
    move1 = (2,1)
    move2 = (5,5)
    number_of_clusters = 3

    # Use k-means with 3 clusters

    clustering = ClusteringWrapper(
        DistanceClass=ChebyshevDistance,
        ClusteringClass=KMeansClustering
    )

    
    print(clustering.get_distance(move1, move2))
    print(clustering.get_clusters([(1,1),(2,2),(3,3)], number_of_clusters))

     

if __name__ == "__main__":
    main()
