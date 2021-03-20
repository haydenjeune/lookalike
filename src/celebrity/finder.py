from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import requests


class ListDownloadException(Exception):
    pass


class CelebrityListFinder(ABC):
    @abstractmethod
    def find(self) -> List[str]:
        pass


@dataclass
class UrlCelebrityListFinder(CelebrityListFinder):
    """
    Downloads a newline delimited text file from a given url to generate a list of celeb names
    """

    list_url: str = r"https://raw.githubusercontent.com/prateekmehta59/Celebrity-Face-Recognition-Dataset/master/List%20of%20Celebrities"

    def find(self) -> List[str]:
        resp = requests.get(self.list_url)
        if resp.status_code != 200:
            raise ListDownloadException(
                f"Received {resp.status_code} from {resp.url} with content: {resp.content}"
            )

        raw_list = resp.content.strip().decode("unicode-escape").split("\n")
        return [name.title().strip() for name in raw_list]
