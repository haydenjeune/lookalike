import environ
import os


@environ.config()
class Config:
    STORAGE_ROOT = environ.var(
        name="STORAGE_ROOT",
        default="file:///Users/hayden.jeune/.celebstore/worker2",
    )
    MAX_VECTORS_PER_PERSON = environ.var(
        name="MAX_VECTORS_PER_PERSON", default="3", converter=int
    )
    MAIN_IMAGE_KEY = environ.var(
        name="MAIN_IMAGE_KEY",
        default="main",
    )
    MAX_WEB_IMAGE_SIZE = environ.var(
        name="MAX_WEB_IMAGE_SIZE", default="512", converter=int
    )
    EXTRACTION_QUEUE_URL = environ.var(
        name="EXTRACTION_QUEUE_URL",
        default="https://sqs.ap-southeast-2.amazonaws.com/311908471898/lookalike-extraction-queue",
    )


def get_config() -> Config:
    return environ.to_config(Config, os.environ)