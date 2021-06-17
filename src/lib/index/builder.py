from abc import ABC, abstractmethod
from typing import List, Optional

from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
from torch import no_grad
from numpy import ndarray, array, median
from numpy.linalg import norm


class FaceNotFound(Exception):
    pass


class ImageVectoriser(ABC):
    @abstractmethod
    def vectorise(self, image: Image.Image) -> ndarray:
        pass


class FaceNetPyTorchImageVectoriser(ImageVectoriser):
    def __init__(self):
        self.face_detector = MTCNN(margin=20, select_largest=True)
        self.face_vectoriser = InceptionResnetV1(pretrained="vggface2").eval()

    @no_grad()
    def vectorise(self, image: Image.Image) -> Optional[ndarray]:
        # Get cropped and prewhitened image tensor
        cropped = self.face_detector(image)
        if cropped is None:
            return None

        # Calculate embedding (unsqueeze to add batch dimension, squeeze to remove it again)
        vec = self.face_vectoriser(cropped.unsqueeze(0)).squeeze()

        return vec.numpy()


class VectorAggregator(ABC):
    @abstractmethod
    def aggregate(self, vectors: List[ndarray]) -> ndarray:
        pass


class MedianVectorAggregator(VectorAggregator):
    def aggregate(self, vectors: List[ndarray]) -> ndarray:
        combined = median(array(vectors), axis=0)
        return combined / norm(combined)