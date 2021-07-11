import environ
import os


@environ.config()
class Config:
    EXTRACTION_QUEUE_URL = environ.var(
        name="EXTRACTION_QUEUE_URL",
        default="https://sqs.ap-southeast-2.amazonaws.com/311908471898/lookalike-extraction-queue",
    )


def get_config() -> Config:
    return environ.to_config(Config, os.environ)