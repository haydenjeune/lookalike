import numpy as np
import pytest
from lib.index.faiss import FaissIndex


@pytest.fixture
def set_numpy_seed():
    np.random.seed(1234)
    yield


def test_search_after_add(set_numpy_seed):
    idx = FaissIndex(vec_dimensions=16)
    vecs = np.random.random((3, 16)).astype("float32")
    names = ["First", "Second", "Third"]

    idx.add(names, vecs)
    result = idx.search(vecs[1], k=1)

    assert result == [("Second", 1.0)]


def test_search_after_successive_adds(set_numpy_seed):
    idx = FaissIndex(vec_dimensions=16)

    # add once
    vecs = np.random.random((3, 16)).astype("float32")
    names = ["First", "Second", "Third"]
    idx.add(names, vecs)

    # add again
    vecs = np.random.random((3, 16)).astype("float32")
    names = ["Harry", "Betty", "Sally"]
    idx.add(names, vecs)

    result = idx.search(vecs[1], k=1)

    assert result == [("Betty", 1.0)]


def test_search_returns_k_results(set_numpy_seed):
    idx = FaissIndex(vec_dimensions=16)

    # add once
    vecs = np.random.random((5, 16)).astype("float32")
    names = ["First", "Second", "Third", "Fourth", "Fifth"]
    idx.add(names, vecs)

    result = idx.search(vecs[1], k=3)

    assert len(result) == 3
    assert ("Second", 1.0) in result