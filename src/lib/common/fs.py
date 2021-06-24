"""File System related utilities used by the storage classes"""

from string import punctuation, whitespace

name_to_path_translation = str.maketrans("", "", punctuation + whitespace)


def _map_name_to_path(name: str) -> str:
    return name.translate(name_to_path_translation)


def _validate_root(root: str):
    scheme = root.split("://")[0]
    if "://" not in root or scheme not in {"s3", "memory", "file"}:
        raise ValueError(f"Invalid file system scheme {scheme}")