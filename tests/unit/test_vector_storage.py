import numpy as np
import pytest

from lib.vector.storage import FsVectorStorage


def test_retrieve_after_persist():
    data = np.array([1, 2, 3, 4])
    sut = FsVectorStorage("memory://test")

    sut.persist("Sally Britty 1", data)
    read_data = sut.retrieve("Sally Britty 1")

    assert (data == read_data).all()


def test_retrieve_without_persist():
    sut = FsVectorStorage("memory://test")

    read_data = sut.retrieve("Sally Britty 2")

    assert read_data is None


@pytest.mark.parametrize("root", ["invalid://test", "test"])
def test_fsvectorstorage_with_invalid_scheme(root):
    with pytest.raises(ValueError):
        sut = FsVectorStorage(root)