import environ
import os


@environ.config()
class Config:
    VECTOR_STORAGE_ROOT = environ.var(
        name="VECTOR_STORAGE_ROOT",
        default="file:///Users/hayden.jeune/.celebstore/worker2",
    )
    IMAGE_STORAGE_ROOT = environ.var(
        name="IMAGE_STORAGE_ROOT",
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


def get_config() -> Config:
    return environ.to_config(Config, os.environ)