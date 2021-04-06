import os
import environ
from pathlib import Path

VECTOR_INDEX_FILEPATH = "VECTOR_INDEX_FILEPATH"


@environ.config()
class Config:
    vector_index_filepath = environ.var(
        name=VECTOR_INDEX_FILEPATH, default="/Users/hayden.jeune/.celebstore/vec"
    )


def get() -> Config:
    return environ.to_config(Config, os.environ)