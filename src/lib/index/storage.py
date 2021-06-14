from abc import ABC
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union, Tuple
import json

from numpy import ndarray, array


class IndexFileException(Exception):
    pass


class VectorIndex(ABC):
    def __init__(self, storage_dir: Union[str, Path]):
        self.storage_file = Path(storage_dir) / "vectors.json"

        # make the desired dir if it doesn't exist
        if not self.storage_file.parent.exists():
            try:
                self.storage_file.parent.mkdir()
            except OSError as e:
                raise IndexFileException(f"Failed to create index directory {self.storage_file.parent}")

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