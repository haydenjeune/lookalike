import pytest
from mock import patch
from io import BytesIO

from PIL import Image

from lib.image.storage import FsImageStorage, LocalImageStorageException


def test_retrieve_after_persist():
    sut = FsImageStorage("memory://test")
    with open("tests/assets/my-profile.jpeg", "rb") as f:
        img = Image.open(f)
        img.load()

    sut.persist("Sally Britty 1", "key", img)
    read_data = sut.retrieve("Sally Britty 1", "key")

    # cant check the actual pixel values as the image is reencoded as jpeg on write
    assert img.size == read_data.size


def test_exists_after_persist():
    sut = FsImageStorage("memory://test")
    with open("tests/assets/my-profile.jpeg", "rb") as f:
        img = Image.open(f)
        img.load()

    sut.persist("Sally Britty 2", "key", img)

    assert sut.exists("Sally Britty 2", "key") == True

def test_duplicate_persist():
    sut = FsImageStorage("memory://test")
    with open("tests/assets/my-profile.jpeg", "rb") as f:
        img = Image.open(f)
        img.load()
    sut.persist("Sally Britty 2.1", "key", img)

    new_img = img.crop((0,0,10,10))
    sut.persist("Sally Britty 2.1", "key", new_img)
    read_data = sut.retrieve("Sally Britty 2.1", "key")

    assert new_img.size == read_data.size

def test_retrieve_without_persist():
    sut = FsImageStorage("memory://test")
    read_data = sut.retrieve("Sally Britty 3", "key")
    assert read_data is None


def test_exists_without_persist():
    sut = FsImageStorage("memory://test")
    assert sut.exists("Sally Britty 4", "key") == False


def test_retrieve_throws_with_bad_data():
    with patch("lib.image.storage.fsspec_open") as m:
        m.return_value = BytesIO(b"this is not image data")
        sut = FsImageStorage("memory://test")

        with pytest.raises(LocalImageStorageException):
            sut.retrieve("Sally Britty 5", "key")


@pytest.mark.parametrize("root", ["invalid://test", "test"])
def test_fsvectorstorage_with_invalid_scheme(root):
    with pytest.raises(ValueError):
        sut = FsImageStorage(root)