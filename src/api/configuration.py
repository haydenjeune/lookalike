import environ
import os


@environ.config()
class Config:
    MAXIMUM_IMAGE_PIXELS = environ.var(
        name="MAXIMUM_IMAGE_PIXELS", default="5000000", converter=int
    )
    INDEX_SERVICE_ADDR = environ.var(
        name="INDEX_SERVICE_ADDR", default="localhost:5051"
    )


def get_config() -> Config:
    return environ.to_config(Config, os.environ)