import pytest

from lib.storage.metadata import FsMetadataStorage


def test_retrieve_after_persist():
    data = {"key": "value"}
    sut = FsMetadataStorage("memory://test")

    sut.persist("Sally Britty 1", data)
    read_data = sut.retrieve("Sally Britty 1")

    assert data == read_data


def test_retrieve_without_persist():
    sut = FsMetadataStorage("memory://test")

    read_data = sut.retrieve("Sally Britty 2")

    assert read_data is None


@pytest.mark.parametrize("root", ["invalid://test", "test"])
def test_fsvectorstorage_with_invalid_scheme(root):
    with pytest.raises(ValueError):
        sut = FsMetadataStorage(root)