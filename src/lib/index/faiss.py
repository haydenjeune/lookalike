from typing import List, Optional, Tuple
from pathlib import Path

import faiss
import numpy as np


class FaissIndex:
    """An index for efficiently searching dense vectors

    Thread safe if add is not called concurrently. faiss will release the GIL
    so multithreaded usage can use multiple cores.
    """

    def __init__(self, vec_dimensions: int = 512, from_dir: Optional[str] = None):
        if from_dir:
            path = Path(from_dir)
            self.index = faiss.read_index(str(path / "index"))
            with open(path / "names.txt", "r") as f:
                self.name_lookup = f.read().splitlines()
        else:
            self.index = faiss.IndexIDMap(faiss.IndexFlatL2(vec_dimensions))
            self.name_lookup: List[str] = []

    def add(self, names: List[str], vector: np.ndarray):
        n_vecs, n_dims = vector.shape
        if n_dims != self.index.d:
            raise ValueError("Given vectors have incorrect dimensionality")
        elif len(names) != n_vecs:
            raise ValueError(
                "Number of names and first dimension of vector array do not match"
            )

        next_id = len(self.name_lookup)
        ids = np.arange(next_id, next_id + n_vecs)
        # for some reason PyRight gets the function signature wrong
        self.index.add_with_ids(vector, ids)  # type: ignore
        self.name_lookup.extend(names)

    def search(self, vector: np.ndarray, k: int = 5) -> List[Tuple[str, float]]:
        n_dims = vector.shape[0]
        if n_dims != self.index.d:
            raise ValueError("Given vector has incorrect dimensionality")

        vector = np.expand_dims(vector, axis=0)
        # for some reason PyRight gets the function signature wrong
        D, I = self.index.search(vector, k)  # type: ignore

        names = [self.name_lookup[i] for i in I.squeeze(axis=0)]
        similarity = [-(dist / 2) + 1 for dist in D.squeeze(axis=0)]

        return list(zip(names, similarity))

    def save(self, dir: str):
        path = Path(dir)
        path.mkdir(exist_ok=True)

        faiss.write_index(self.index, str(path / "index"))
        with open(path / "names.txt", "w") as f:
            f.write("\n".join(self.name_lookup))
