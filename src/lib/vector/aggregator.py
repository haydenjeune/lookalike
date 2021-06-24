from abc import ABC, abstractmethod
from typing import List

from numpy import ndarray, array, median
from numpy.linalg import norm


class VectorAggregator(ABC):
    @abstractmethod
    def aggregate(self, vectors: List[ndarray]) -> ndarray:
        pass


class MedianVectorAggregator(VectorAggregator):
    def aggregate(self, vectors: List[ndarray]) -> ndarray:
        combined = median(array(vectors), axis=0)
        return combined / norm(combined)