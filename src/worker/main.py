from loguru import logger

from worker.configuration import get_config
from lib.image.retrieve import ImageRetriever
from lib.image.retrieve import ImageRetrieverException, WikipediaImageRetriever


config = get_config()


class ImageProcessor:
    def __init__(self, image_retriever: ImageRetriever) -> None:
        self.image_retriever = image_retriever

    def process(self, name: str):
        try:
            images = self.image_retriever.retrieve(
                name, max_images=config.MAX_IMAGES_PER_PERSON
            )
        except ImageRetrieverException as e:
            logger.error(f"Unrecoverable error retrieving images for {name}")
            # TODO: put to DLQ
            return

        for image in images:
            image.show()


def main():
    processor = ImageProcessor(WikipediaImageRetriever())
    processor.process("Morgan Freeman")


if __name__ == "__main__":
    logger.info("Starting worker...")
    main()