from pathlib import Path

import pytest

from src.celebrity.storage import LocalCelebrityStorage, LocalCelebrityStorageException

# fs comes from the pyfakefs package
def test_local_celebrity_storage_saves_file(fs):
    fake_path = Path("./test")
    storage = LocalCelebrityStorage(storage_root=str(fake_path))
    fs.create_dir(fake_path)

    storage.persist(["me", "you", "everyone else"])

    expected_file_content = "me\nyou\neveryone else"
    assert (
        fs.get_object(fake_path / storage._storage_file_name).contents
        == expected_file_content
    )


def test_local_celebrity_storage_creates_dir_and_saves_file(fs):
    fake_path = Path("./test")
    storage = LocalCelebrityStorage(storage_root=str(fake_path))

    storage.persist(["me", "you", "everyone else"])

    expected_file_content = "me\nyou\neveryone else"
    assert (
        fs.get_object(fake_path / storage._storage_file_name).contents
        == expected_file_content
    )


def test_local_celebrity_storage_raises_on_unwriteable_file(fs):
    fake_path = Path("./test")
    storage = LocalCelebrityStorage(storage_root=str(fake_path))
    fs.create_dir(fake_path)

    # throw an error on writing to the file
    def raise_OSError(f):
        raise OSError()

    fs.create_file(fake_path / storage._storage_file_name, side_effect=raise_OSError)

    with pytest.raises(LocalCelebrityStorageException):
        storage.persist(["me", "you", "everyone else"])

def test_local_celebrity_storage_raises_on_insufficient_permissions(fs):
    fake_path = Path("./test/dir")
    storage = LocalCelebrityStorage(storage_root=str(fake_path))
    fs.create_dir(fake_path.parent, perm_bits=000)

    with pytest.raises(LocalCelebrityStorageException):
        storage.persist(["me", "you", "everyone else"])
