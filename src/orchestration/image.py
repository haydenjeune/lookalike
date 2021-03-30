from dataclasses import dataclass
from tqdm import tqdm

from src.image.storage import LocalImageStorage
from src.celebrity.storage import LocalCelebrityStorage
from src.image.retrieve import ImageRetrieverException, WikipediaImageRetriever
from src.orchestration.base import Orchestrator


@dataclass
class LocalImageDownloader(Orchestrator):
    storage_path: str = "/Users/hayden.jeune/.celebstore"

    def run(self):
        celeb_storage = LocalCelebrityStorage(self.storage_path)
        celebs = celeb_storage.retrieve()

        wikipedia = WikipediaImageRetriever()
        image_storage = LocalImageStorage(self.storage_path + "/images")

        for name in tqdm(celebs):
            try:
                for i, image in enumerate(wikipedia.retrieve(name)):
                    image_storage.persist(name, str(i), image)
            except ImageRetrieverException as e:
                print(str(e))
            except Exception as e:
                print(f"Error in {name}: str(e)")