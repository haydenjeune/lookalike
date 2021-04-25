import environ
import os


VECTOR_INDEX_FILEPATH = "VECTOR_INDEX_FILEPATH"
MAXIMUM_IMAGE_PIXELS = "MAXIMUM_IMAGE_PIXELS"


@environ.config()
class Config:
    vector_index_filepath = environ.var(
        name=VECTOR_INDEX_FILEPATH, default="/Users/hayden.jeune/.celebstore/vec"
    )
    max_image_pixels = environ.var(
        name=MAXIMUM_IMAGE_PIXELS, default="5000000", converter=int
    )


def get() -> Config:
    return environ.to_config(Config, os.environ)