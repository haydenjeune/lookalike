"""Metadata storage utilities"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from json import dump, load

from fsspec import open as fsspec_open

from lib.common.fs import _map_name_to_path, _validate_root


class MetadataStorage(ABC):
    @abstractmethod
    def persist(self, celebrity_name: str, metadata: Dict[str, str]):
        pass

    @abstractmethod
    def retrieve(self, celebrity_name: str) -> Optional[Dict[str, str]]:
        pass

    @abstractmethod
    def exists(self, celebrity_name: str) -> bool:
        pass


class FsMetadataStorage(MetadataStorage):
    def __init__(self, root: str):
        _validate_root(root)
        self.root = root

    def _build_path(self, celebrity_name: str) -> str:
        return f"{self.root}/{_map_name_to_path(celebrity_name)}/meta.json"

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

    def exists(self, celebrity_name: str) -> bool:
        path = self._build_path(celebrity_name)
        try:
            with fsspec_open(path, "r") as f:
                # just enter the context and check for the exception
                return True
        except FileNotFoundError:
            return False