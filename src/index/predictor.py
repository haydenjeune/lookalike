from abc import ABC, abstractmethod, abstractstaticmethod
from typing import List, Optional, Type
from dataclasses import dataclass, field

from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
from torch import no_grad
from numpy import ndarray, dot

from index.builder import FaceNetPyTorchImageVectoriser, ImageVectoriser
from index.storage import VectorIndex


class FaceNotFound(Exception):
    pass


@dataclass
class Result:
    name: str
    similarity: float


class Comparator(ABC):
    @abstractstaticmethod
    def compare(l: ndarray, r: ndarray) -> float:
        raise NotImplementedError()


class DotProductComparator(Comparator):
    """Returns a dot product of the input vectors scaled between 0 and 1.

    Assumes both input vectors are unit vectors of equal dimensionality.
    """

    @staticmethod
    def compare(l: ndarray, r: ndarray) -> float:
        return (dot(l, r) + 1) / 2


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
            # TODO: do this properly
            return []

        similarities = [
            (self.comparator.compare(img_vec, celeb_vec), name)
            for name, celeb_vec in self.index.vectors
        ]
        # TODO: there are more efficient ways to do this
        similarities.sort(key=lambda x: x[0], reverse=True)

        return [Result(name, score) for score, name in similarities[: self.num_results]]
