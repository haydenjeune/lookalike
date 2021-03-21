from dataclasses import dataclass
from logging import getLogger

from src.celebrity.storage import LocalCelebrityStorage
from src.image.storage import LocalImageStorage
from src.index.builder import FaceNetPyTorchImageVectoriser, FaceNotFound
from src.index.storage import VectorIndex
from src.orchestration.base import Orchestrator

from tqdm import tqdm

log = getLogger(__name__)


@dataclass
class ImagePreProcessing(Orchestrator):
    storage_path: str = "/Users/hayden.jeune/.celebstore"

    def run(self):
        celeb_storage = LocalCelebrityStorage(self.storage_path)
        celebs = celeb_storage.retrieve()
        image_storage = LocalImageStorage(self.storage_path + "/images")
        index = VectorIndex(self.storage_path + "/vec")
        vectoriser = FaceNetPyTorchImageVectoriser()

        for name in tqdm(celebs):
            if image_storage.exists(name):
                try:
                    im = image_storage.retrieve(name)
                    vec = vectoriser.vectorise(im)
                    index.add(name, vec)
                except Exception as e:
                    log.exception(f"Error occured processing {name}: {e}")
            else:
                print(f"{name} not found")
        index.save()
