from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List


class LocalCelebrityStorageException(Exception):
    pass


class CelebrityStorage(ABC):
    @abstractmethod
    def persist(self, celebrities: List[str]):
        pass


@dataclass
class LocalCelebrityStorage(CelebrityStorage):
    """
    Persists a list of celebrities on local disk.

    Will attempt to create the directory at storage_root if it doesn't exist.
    """

    storage_root: str
    _storage_file_name: str = "celebrities.txt"

    def persist(self, celebrities: List[str]):
        path = Path(self.storage_root).resolve()
        try:
            if not path.exists():
                path.mkdir()
        except OSError as e:
            raise LocalCelebrityStorageException(
                "Failed to create storage directory"
            ) from e

        try:
            with open(path / self._storage_file_name, "w") as f:
                f.write("\n".join(celebrities))
        except OSError as e:
            raise LocalCelebrityStorageException(
                "Failed to write to storage file"
            ) from e
