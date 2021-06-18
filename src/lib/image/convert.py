from abc import ABC
from dataclasses import dataclass

from PIL import Image


class ImageConverter(ABC):
    def convert(self, image: Image.Image) -> Image.Image:
        raise NotImplementedError()


@dataclass
class ImageResizer(ImageConverter):
    max_size: int = 512

    def convert(self, image: Image.Image) -> Image.Image:
        width, height = image.size
        if width <= self.max_size and height <= self.max_size:
            return image

        ratio = max(width / self.max_size, height / self.max_size)

        new_width = int(width // ratio)
        new_height = int(height // ratio)

        return image.resize((new_width, new_height))
