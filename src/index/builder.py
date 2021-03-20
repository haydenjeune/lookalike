from abc import ABC, abstractmethod
from typing import List

from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
from torch import no_grad
from numpy import ndarray


class ImageVectoriser(ABC):
    @abstractmethod
    def vectorise(self, image: Image.Image) -> List[float]:
        pass


class FaceNetPyTorchImageVectoriser(ImageVectoriser):
    def __init__(self):
        self.face_detector = MTCNN(margin=20, select_largest=True)
        self.face_vectoriser = InceptionResnetV1(pretrained="vggface2").eval()

    @no_grad()
    def vectorise(self, image: Image.Image) -> ndarray:
        # Get cropped and prewhitened image tensor
        cropped = self.face_detector(image)

        # Calculate embedding (unsqueeze to add batch dimension, squeeze to remove it again)
        vec = self.face_vectoriser(cropped.unsqueeze(0)).squeeze()

        return vec.numpy()