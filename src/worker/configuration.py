import environ
import os


@environ.config()
class Config:
    VECTOR_INDEX_FILEPATH = environ.var(
        name="VECTOR_INDEX_FILEPATH", default="/Users/hayden.jeune/.celebstore/vec"
    )
    MAXIMUM_IMAGE_PIXELS = environ.var(
        name="MAXIMUM_IMAGE_PIXELS", default="5000000", converter=int
    )
    MAX_VECTORS_PER_PERSON = environ.var(
        name="MAX_VECTORS_PER_PERSON", default="3", converter=int
    )


def get_config() -> Config:
    return environ.to_config(Config, os.environ)