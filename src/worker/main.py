import csv
from loguru import logger

from worker.configuration import get_config
from lib.image.retrieve import (
    ImageRetriever,
    ImageRetrieverException,
    WikipediaImageRetriever,
)
from lib.index.builder import (
    ImageVectoriser,
    FaceNetPyTorchImageVectoriser,
    VectorAggregator,
    MedianVectorAggregator,
)


config = get_config()


class ImageProcessor:
    def __init__(
        self,
        image_retriever: ImageRetriever,
        image_vectoriser: ImageVectoriser,
        vector_aggregator: VectorAggregator,
    ) -> None:
        self.image_retriever = image_retriever
        self.image_vectoriser = image_vectoriser
        self.vector_aggregator = vector_aggregator

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

            vectors.append(vector)

        if len(vectors) == 0:
            logger.error(f"No face vectors found for {name}")
            # TODO: put to DLQ
            return

        aggregated_vector = self.vector_aggregator.aggregate(vectors)
        # TODO: some quality checks?

        logger.info(f"{aggregated_vector[:5]}")


def main():

    processor = ImageProcessor(
        WikipediaImageRetriever(),
        FaceNetPyTorchImageVectoriser(),
        MedianVectorAggregator(),
    )

    with open("/Users/hayden.jeune/Downloads/name.basics.tsv") as file:
        reader = csv.reader(file, delimiter="\t")
        for i, row in enumerate(reader):
            if i > 100:
                break
            elif i < 83:
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
