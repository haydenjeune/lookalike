import boto3
from loguru import logger

from lib.common.metadata import FsMetadataStorage, MetadataStorage
from worker.configuration import get_config
from lib.image.retrieve import (
    ImageRetriever,
    WikipediaImageRetriever,
)
from lib.image.storage import FsImageStorage, ImageStorage
from lib.image.convert import ImageResizer
from lib.model.facenet import (
    ImageVectoriser,
    FaceNetPyTorchImageVectoriser,
)
from lib.vector.aggregator import (
    VectorAggregator,
    MedianVectorAggregator,
)
from lib.vector.storage import (
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
        metadata_storage: MetadataStorage,
    ) -> None:
        self.image_retriever = image_retriever
        self.image_vectoriser = image_vectoriser
        self.image_resizer = image_resizer
        self.image_storage = image_storage
        self.vector_aggregator = vector_aggregator
        self.vector_storage = vector_storage
        self.metadata_storage = metadata_storage

    def process(self, name: str):
        """Stores a key image and a face vector given a celebrities name

        Throws:
            lib.image.retrieve.ImageRetrieverException
        """
        # do not proceed if we've already done this celeb
        if self.metadata_storage.exists(name):
            logger.info(f"Skipping {name}: Already done")
            return

        metadata = {"name": name, "images": []}

        vectors = []
        for image, location in self.image_retriever.retrieve(name):
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
            metadata["images"].append(location)

        if len(vectors) == 0:
            logger.error(f"No face vectors found for {name}")
        else:
            # TODO: some quality checks?
            aggregated_vector = self.vector_aggregator.aggregate(vectors)
            self.vector_storage.persist(name, aggregated_vector)

        self.metadata_storage.persist(name, metadata)


def main():
    processor = ImageProcessor(
        WikipediaImageRetriever(),
        FaceNetPyTorchImageVectoriser(),
        ImageResizer(config.MAX_WEB_IMAGE_SIZE),
        FsImageStorage(config.STORAGE_ROOT),
        MedianVectorAggregator(),
        FsVectorStorage(config.STORAGE_ROOT),
        FsMetadataStorage(config.STORAGE_ROOT),
    )

    sqs = boto3.resource("sqs")
    queue = sqs.Queue(config.EXTRACTION_QUEUE_URL)

    counter = 0

    while True:
        messages = queue.receive_messages(MaxNumberOfMessages=3, WaitTimeSeconds=20)
        logger.info(f"Received {len(messages)} messages from queue")

        # handle empty message limit
        if len(messages) == 0:
            counter += 1
        else:
            counter = 0
        if (
            config.CONSECUTIVE_EMPTY_MESSAGE_LIMIT != -1
            and counter > config.CONSECUTIVE_EMPTY_MESSAGE_LIMIT
        ):
            logger.info("Reached consecutive empty message limit. Exiting.")
            return

        for message in messages:
            logger.info(f"Received message: {message.body}")
            name = message.body
            try:
                processor.process(name)
            except Exception as e:
                logger.error(f"Failed to process {name}: {e}")
            finally:
                message.delete()


if __name__ == "__main__":
    logger.info("Starting worker...")
    main()
