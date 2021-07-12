import environ
import os


@environ.config()
class Config:
    STORAGE_ROOT = environ.var(
        name="STORAGE_ROOT",
        default="/Users/hayden.jeune/.celebstore/worker3",
    )
    INDEX_ROOT = environ.var(
        name="STORAGE_ROOT",
        default="/Users/hayden.jeune/.celebstore/index3",
    )


def get_config() -> Config:
    return environ.to_config(Config, os.environ)