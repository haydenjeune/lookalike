from abc import ABC, abstractmethod
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from pathlib import Path
from string import punctuation, whitespace
from typing import Dict, Iterable, List, Optional, Union, Tuple
import json
from urllib.parse import urlparse

from fsspec import open as fsspec_open
from fsspec.spec import AbstractFileSystem
from numpy import ndarray, array, save, load


class IndexFileException(Exception):
    pass


class VectorIndex:
    def __init__(self, storage_dir: Union[str, Path]):
        self.storage_file = Path(storage_dir) / "vectors.json"

        # make the desired dir if it doesn't exist
        if not self.storage_file.parent.exists():
            try:
                self.storage_file.parent.mkdir()
            except OSError as e:
                raise IndexFileException(
                    f"Failed to create index directory {self.storage_file.parent}"
                )

        # for now we use List[float] in json even though it's inefficient
        # eventually I'll serialise the ndarray to bytes or something
        self._vectors: Dict[str, List[float]] = self.load()

    @property
    def vectors(self) -> List[Tuple[str, ndarray]]:
        return [(name, array(vec)) for name, vec in self._vectors.items()]

    def load(self) -> Dict[str, List[float]]:
        # read file
        try:
            with open(self.storage_file, "r") as f:
                content = f.read()
        except FileNotFoundError as e:
            return {}
        except OSError as e:
            raise IndexFileException("Error reading index file") from e

        # parse file
        try:
            return json.loads(content)
        except JSONDecodeError as e:
            raise IndexFileException("Error parsing index file")

    def add(self, celebrity_name: str, vector: ndarray):
        self._vectors[celebrity_name] = vector.tolist()

    def get(self, celebrity_name: str) -> Optional[ndarray]:
        return array(self._vectors.get(celebrity_name, None))

    def save(self):
        try:
            with open(self.storage_file, "w") as f:
                f.write(json.dumps(self._vectors))
        except OSError:
            IndexFileException("Failed to write to index file")


class VectorStorage(ABC):
    @abstractmethod
    def persist(self, celebrity_name: str, vector: ndarray):
        pass

    @abstractmethod
    def retrieve(self, celebrity_name: str) -> ndarray:
        pass


name_to_path_translation = str.maketrans("", "", punctuation + whitespace)


class FsVectorStorage(VectorStorage):
    def __init__(self, root: str):
        self._validate_root(root)
        self.root = root

    @staticmethod
    def _validate_root(root: str):
        scheme = root.split("://")[0]
        if "://" not in root or scheme not in {"s3", "memory", "file"}:
            raise ValueError(f"Invalid file system scheme {scheme}")

    def persist(self, celebrity_name: str, vector: ndarray):
        path = (
            f"{self.root}/{celebrity_name.translate(name_to_path_translation)}/vec.npy"
        )
        with fsspec_open(path, "wb") as f:
            save(f, vector, allow_pickle=False)

    def retrieve(self, celebrity_name: str) -> Optional[ndarray]:
        path = (
            f"{self.root}/{celebrity_name.translate(name_to_path_translation)}/vec.npy"
        )
        try:
            with fsspec_open(path, "rb") as f:
                vector = load(f, allow_pickle=False)
        except FileNotFoundError:
            return None

        if not isinstance(vector, ndarray):
            return None

        return vector
