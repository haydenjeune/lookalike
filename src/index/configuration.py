import environ
import os


@environ.config()
class Config:
    INDEX_ROOT = environ.var(
        name="INDEX_ROOT",
        default="/Users/hayden.jeune/.celebstore/index3",
    )
    INDEX_VECTOR_DIMENSIONS = environ.var(
        name="INDEX_VECTOR_DIMENSIONS",
        default="512",
        converter=int,
    )
    MAX_WORKERS = environ.var(
        name="MAX_WORKERS",
        default="10",
        converter=int,
    )
    ADDRESS = environ.var(
        name="ADDRESS",
        default="[::]:5051",
    )


def get_config() -> Config:
    return environ.to_config(Config, os.environ)