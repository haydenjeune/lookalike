from abc import ABC, abstractmethod
from typing import Dict, Optional
from json import dump, load
from string import punctuation, whitespace

from fsspec import open as fsspec_open


class MetadataStorage(ABC):
    @abstractmethod
    def persist(self, celebrity_name: str, metadata: Dict[str, str]):
        pass

    @abstractmethod
    def retrieve(self, celebrity_name: str) -> Optional[Dict[str, str]]:
        pass


name_to_path_translation = str.maketrans("", "", punctuation + whitespace)


class FsMetadataStorage(MetadataStorage):
    def __init__(self, root: str):
        self._validate_root(root)
        self.root = root

    @staticmethod
    def _validate_root(root: str):
        scheme = root.split("://")[0]
        if "://" not in root or scheme not in {"s3", "memory", "file"}:
            raise ValueError(f"Invalid file system scheme {scheme}")

    def _build_path(self, celebrity_name: str) -> str:
        return f"{self.root}/{celebrity_name.translate(name_to_path_translation)}/meta.json"

    def persist(self, celebrity_name: str, metadata: Dict[str, str]):
        path = self._build_path(celebrity_name)
        with fsspec_open(path, "w") as f:
            dump(metadata, f)

    def retrieve(self, celebrity_name: str) -> Optional[Dict[str, str]]:
        path = self._build_path(celebrity_name)
        try:
            with fsspec_open(path, "r") as f:
                return load(f)
        except FileNotFoundError:
            return None