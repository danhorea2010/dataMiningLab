from abc import abstractmethod,ABC
from typing import List,Tuple

class MeanCalculator(ABC):
    @classmethod
    @abstractmethod
    def mean(points: List[Tuple[int, int]]) -> Tuple[float, float]:
        pass


class Mean(MeanCalculator): 
    def mean(points: List[Tuple[int, int]]) -> Tuple[float, float]:
        """Computes the mean of a list of points."""
        if not points:
            return (0,0)

        n = len(points)
        mean_x = sum([point[0] for point in points]) / n
        mean_y = sum([point[1] for point in points]) / n
        return (mean_x, mean_y)