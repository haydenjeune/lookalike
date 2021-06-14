from abc import ABC, abstractmethod, abstractstaticmethod
from typing import Any, Callable, List, Type, TypeVar
from dataclasses import dataclass, field
from random import randrange

from PIL import Image
from numpy import ndarray, dot, add

from lib.index.builder import FaceNetPyTorchImageVectoriser, ImageVectoriser
from lib.index.storage import VectorIndex

T = TypeVar("T")


class FaceNotFound(Exception):
    pass


@dataclass
class Result:
    name: str
    similarity: float


class Comparator(ABC):
    @staticmethod
    @abstractmethod
    def compare(l: ndarray, r: ndarray) -> float:
        raise NotImplementedError()


class DotProductComparator(Comparator):
    """Returns a dot product of the input vectors scaled between 0 and 1.

    Assumes both input vectors are unit vectors of equal dimensionality.
    """

    @staticmethod
    def compare(l: ndarray, r: ndarray) -> float:
        return add(dot(l, r), 1) / 2


@dataclass
class Predictor(ABC):
    index: VectorIndex
    comparator: Comparator
    vectoriser: ImageVectoriser

    @abstractmethod
    def predict(self, image: Image.Image) -> Result:
        pass


@dataclass
class FaceNetDotProductPredictor(Predictor):
    index: VectorIndex
    comparator: Type = field(default=DotProductComparator)
    vectoriser: FaceNetPyTorchImageVectoriser = field(
        default_factory=FaceNetPyTorchImageVectoriser
    )
    num_results: int = 5

    def predict(self, image: Image.Image) -> List[Result]:
        img_vec = self.vectoriser.vectorise(image)
        if img_vec is None:
            return []

        all_similarities = [
            (self.comparator.compare(img_vec, celeb_vec), name)
            for name, celeb_vec in self.index.vectors
        ]

        top_similarities = top_k(
            all_similarities, k=self.num_results, key=lambda x: x[0]
        )

        return [Result(name, score) for score, name in top_similarities]


def top_k(items: List[T], k: int, key: Callable[[T], float]):
    # use quickselect variant to get average case O(n) selection of k items where n=len(items)
    # https://en.wikipedia.org/wiki/Quickselect
    if k > len(items):
        return items

    left = 0
    right = len(items) - 1

    while True:
        if left == right:
            return items[:k]

        pivot_index = randrange(left, right)
        pivot_index = partition(items, left, right, pivot_index, key)

        if pivot_index in {k, k - 1}:
            return items[:k]
        elif pivot_index > k:
            right = pivot_index - 1
        elif pivot_index < k - 1:
            left = pivot_index + 1


def partition(
    items: List[T],
    left: int,
    right: int,
    pivot_index: int,
    key: Callable[[T], float],
):
    pivot_value = key(items[pivot_index])

    # swap pivot element to end
    items[pivot_index], items[right] = items[right], items[pivot_index]

    store_index = left

    for i in range(left, right):
        if key(items[i]) > pivot_value:
            items[store_index], items[i] = items[i], items[store_index]
            store_index += 1

    # swap pivot back to partition boundary
    items[store_index], items[right] = items[right], items[store_index]

    return store_index
