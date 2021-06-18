import csv
from PIL import Image
from loguru import logger
from lib.image.storage import FsImageStorage, ImageStorage

from worker.configuration import get_config
from lib.image.retrieve import (
    ImageRetriever,
    WikipediaImageRetriever,
)
from lib.image.convert import ImageResizer
from lib.index.builder import (
    ImageVectoriser,
    FaceNetPyTorchImageVectoriser,
    VectorAggregator,
    MedianVectorAggregator,
)
from lib.index.storage import (
    VectorStorage,
    FsVectorStorage,
)


config = get_config()


class ImageProcessor:
    def __init__(
        self,
        image_retriever: ImageRetriever,
        image_vectoriser: ImageVectoriser,
        image_resizer: ImageResizer,
        image_storage: ImageStorage,
        vector_aggregator: VectorAggregator,
        vector_storage: VectorStorage,
    ) -> None:
        self.image_retriever = image_retriever
        self.image_vectoriser = image_vectoriser
        self.image_resizer = image_resizer
        self.image_storage = image_storage
        self.vector_aggregator = vector_aggregator
        self.vector_storage = vector_storage

    def process(self, name: str):
        """Stores a key image and a face vector given a celebrities name

        Throws:
            lib.image.retrieve.ImageRetrieverException
        """
        images = self.image_retriever.retrieve(name)

        vectors = []
        for image in images:
            if len(vectors) >= config.MAX_VECTORS_PER_PERSON:
                break

            vector = self.image_vectoriser.vectorise(image)
            if vector is None:
                continue

            # store the first image with a face as the key image
            if len(vectors) == 0:
                web_image = self.image_resizer.convert(image)
                self.image_storage.persist(name, config.MAIN_IMAGE_KEY, web_image)

            vectors.append(vector)

        if len(vectors) == 0:
            logger.error(f"No face vectors found for {name}")
            # TODO: put to DLQ
            return

        aggregated_vector = self.vector_aggregator.aggregate(vectors)
        # TODO: some quality checks?

        self.vector_storage.persist(name, aggregated_vector)


def main():
    processor = ImageProcessor(
        WikipediaImageRetriever(),
        FaceNetPyTorchImageVectoriser(),
        ImageResizer(config.MAX_WEB_IMAGE_SIZE),
        FsImageStorage(config.IMAGE_STORAGE_ROOT),
        MedianVectorAggregator(),
        FsVectorStorage(config.VECTOR_STORAGE_ROOT),
    )

    with open("/Users/hayden.jeune/Downloads/name.basics.tsv") as file:
        reader = csv.reader(file, delimiter="\t")
        for i, row in enumerate(reader):
            if i > 500:
                break
            elif i < 1:
                # skip header
                continue

            name = row[1]

            logger.info(f"[{i}] {name}")
            try:
                processor.process(name)
            except Exception as e:
                logger.error(f"Failed to process {name}: {e}")


if __name__ == "__main__":
    logger.info("Starting worker...")
    main()
