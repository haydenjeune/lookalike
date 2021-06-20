from typing import List, Dict
from pathlib import Path
from json import load as load_json

from loguru import logger
import faiss
from numpy import ndarray, arange
import numpy as np
from numpy import load as load_numpy


from lib.index.index import Index
from indexer.configuration import get_config

config = get_config()


def chunker(seq, size):
    for pos in range(0, len(seq), size):
        yield seq[pos : pos + size]


def get_name(path: Path):
    with open(path / "meta.json", "r") as f:
        data = load_json(f)
        return data["name"]


def get_vector(path: Path):
    with open(path / "vec.npy", "rb") as f:
        return load_numpy(f, allow_pickle=False)


def main():
    root = Path(config.STORAGE_ROOT)

    index = Index(vec_dimensions=512)
    records = list(root.glob("*/"))

    names = [get_name(record) for record in records]
    vectors = np.array([get_vector(record) for record in records])

    index.add(names, vectors)


    index.save(config.INDEX_ROOT)

    new_index = Index(from_dir=config.INDEX_ROOT)

    search_name = names[5]
    search_vec = vectors[5]
    print(f"Looking for {search_name}")
    print("Found:")
    print(new_index.search(search_vec))

if __name__ == "__main__":
    logger.info("Starting indexer...")
    main()
