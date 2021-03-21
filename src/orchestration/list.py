from dataclasses import dataclass

from src.celebrity.finder import UrlCelebrityListFinder
from src.celebrity.storage import LocalCelebrityStorage
from src.orchestration.base import Orchestrator


@dataclass
class LocalListDownloader(Orchestrator):
    url: str = r"https://raw.githubusercontent.com/prateekmehta59/Celebrity-Face-Recognition-Dataset/master/List%20of%20Celebrities"
    storage_path: str = "/Users/hayden.jeune/.celebstore"

    def run(self):
        finder = UrlCelebrityListFinder(list_url=self.url)
        celeb_list = finder.find()

        storage = LocalCelebrityStorage(storage_root=self.storage_path)
        storage.persist(celeb_list)
