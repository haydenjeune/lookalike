from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List
from PIL import Image


class LocalImageStorageException(Exception):
    pass


class ImageNotFound(LocalImageStorageException):
    pass


class ImageStorage(ABC):
    @abstractmethod
    def persist(self, celebrities: List[str]):
        pass


@dataclass
class LocalImageStorage(ImageStorage):
    """
    Persists an image of a celebrity on local disk.

    Will attempt to create the directory at storage_root if it doesn't exist.
    """

    storage_root: str

    def _get_filepath(self, celebrity_name: str) -> Path:
        root = Path(self.storage_root).resolve()
        return root / (celebrity_name + ".jpg")

    def persist(self, celebrity_name: str, image: Image.Image):
        path = Path(self.storage_root).resolve()
        try:
            if not path.exists():
                path.mkdir()
        except OSError as e:
            raise LocalImageStorageException(
                "Failed to create image storage directory"
            ) from e

        try:
            with open(self._get_filepath(celebrity_name), "wb") as f:
                image.convert("RGB").save(f, format="jpeg")
        except OSError as e:
            raise LocalImageStorageException("Failed to write to image file") from e

    def exists(self, celebrity_name: str) -> bool:
        return self._get_filepath(celebrity_name).exists()

    def retrieve(self, celebrity_name: str) -> Image.Image:
        filepath = self._get_filepath(celebrity_name)
        if not filepath.exists():
            raise ImageNotFound(f"No image for {celebrity_name} exists")

        try:
            return Image.open(filepath)
        except OSError as e:
            raise LocalImageStorageException(f"Failed to read image {filepath}") from e
