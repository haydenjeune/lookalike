from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List
from PIL import Image


class LocalImageStorageException(Exception):
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
            with open(path / "images" / celebrity_name / ".jpg", "wb") as f:
                image.save(f, format="jpeg")
        except OSError as e:
            raise LocalImageStorageException("Failed to write to image file") from e
