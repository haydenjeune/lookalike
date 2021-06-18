from abc import ABC, abstractmethod
from typing import Optional
from string import punctuation, whitespace

from fsspec import open as fsspec_open
from PIL import Image, UnidentifiedImageError


class LocalImageStorageException(Exception):
    pass


class ImageStorage(ABC):
    @abstractmethod
    def persist(self, celebrity_name: str, key: str, image: Image.Image):
        pass

    @abstractmethod
    def retrieve(self, celebrity_name: str, key: str) -> Optional[Image.Image]:
        pass

    @abstractmethod
    def exists(self, celebrity_name: str, key: str) -> bool:
        pass


name_to_path_translation = str.maketrans("", "", punctuation + whitespace)


class FsImageStorage(ImageStorage):
    STORAGE_FORMAT = "jpeg"

    def __init__(self, root: str):
        self._validate_root(root)
        self.root = root

    @staticmethod
    def _validate_root(root: str):
        scheme = root.split("://")[0]
        if "://" not in root or scheme not in {"s3", "memory", "file"}:
            raise ValueError(f"Invalid file system scheme {scheme}")

    def _build_path(
        self, celebrity_name: str, key: str, extension: Optional[str]
    ) -> str:
        path = f"{self.root}/{celebrity_name.translate(name_to_path_translation)}/{key}"
        if extension:
            path += f".{extension}"
        return path

    def persist(self, celebrity_name: str, key: str, image: Image.Image):
        path = self._build_path(celebrity_name, key, FsImageStorage.STORAGE_FORMAT)
        with fsspec_open(path, "wb") as f:
            image.save(f, FsImageStorage.STORAGE_FORMAT)

    def retrieve(self, celebrity_name: str, key: str) -> Optional[Image.Image]:
        path = self._build_path(celebrity_name, key, FsImageStorage.STORAGE_FORMAT)
        try:
            with fsspec_open(path, "rb") as f:
                img = Image.open(f)
                img.load()
                return img
        except FileNotFoundError:
            return None
        except UnidentifiedImageError as e:
            raise LocalImageStorageException("Bad image data") from e

    def exists(self, celebrity_name: str, key: str) -> bool:
        path = self._build_path(celebrity_name, key, FsImageStorage.STORAGE_FORMAT)
        try:
            with fsspec_open(path, "rb") as f:
                # just enter the context and check for the exception
                return True
        except FileNotFoundError:
            return False
