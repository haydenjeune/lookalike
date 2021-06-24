from abc import ABC, abstractmethod
from typing import Optional

from fsspec import open as fsspec_open
from numpy import ndarray, save, load

from lib.common.fs import _map_name_to_path, _validate_root


class VectorStorage(ABC):
    @abstractmethod
    def persist(self, celebrity_name: str, vector: ndarray):
        pass

    @abstractmethod
    def retrieve(self, celebrity_name: str) -> ndarray:
        pass


class FsVectorStorage(VectorStorage):
    def __init__(self, root: str):
        _validate_root(root)
        self.root = root

    def _build_path(self, celebrity_name: str) -> str:
        return f"{self.root}/{_map_name_to_path(celebrity_name)}/vec.npy"

    def persist(self, celebrity_name: str, vector: ndarray):
        path = self._build_path(celebrity_name)
        with fsspec_open(path, "wb") as f:
            save(f, vector, allow_pickle=False)

    def retrieve(self, celebrity_name: str) -> Optional[ndarray]:
        path = self._build_path(celebrity_name)
        try:
            with fsspec_open(path, "rb") as f:
                vector = load(f, allow_pickle=False)
        except FileNotFoundError:
            return None

        if not isinstance(vector, ndarray):
            return None

        return vector
