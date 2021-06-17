import environ
import os


@environ.config()
class Config:
    VECTOR_STORAGE_ROOT = environ.var(
        name="VECTOR_STORAGE_ROOT",
        default="file:///Users/hayden.jeune/.celebstore/worker",
    )
    MAX_VECTORS_PER_PERSON = environ.var(
        name="MAX_VECTORS_PER_PERSON", default="3", converter=int
    )


def get_config() -> Config:
    return environ.to_config(Config, os.environ)