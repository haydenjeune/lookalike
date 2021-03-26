from dataclasses import dataclass
from logging import getLogger

from src.celebrity.storage import LocalCelebrityStorage
from src.image.storage import LocalImageStorage
from src.index.builder import (
    FaceNetPyTorchImageVectoriser,
    FaceNotFound,
    MedianVectorAggregator,
)
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
        aggregator = MedianVectorAggregator()

        for name in tqdm(celebs):
            try:
                images = image_storage.retrieve_all(name)
                if len(images) > 0:
                    vectors = []
                    for image in images:
                        vec = vectoriser.vectorise(image)
                        if vec is not None:
                            vectors.append(vec)
                    combined = aggregator.aggregate(vectors)
                    index.add(name, combined)
                else:
                    print(f"{name} not found")
            except Exception as e:
                log.exception(f"Error occured processing {name}: {e}")
        index.save()
