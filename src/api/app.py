from typing import NamedTuple
from connexion import FlaskApp, ProblemException
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from pathlib import Path
from flask_cors import CORS
import base64
from binascii import Error as DecodeError

from api import configuration
from index.predictor import FaceNetDotProductPredictor
from index.storage import VectorIndex

config = configuration.get()
predictor = FaceNetDotProductPredictor(index=VectorIndex(config.vector_index_filepath))


def ping():
    return "pong"


def _deserialise_image(data: bytes) -> Image.Image:
    try:
        data = base64.b64decode(data)
        im = Image.open(BytesIO(data)).convert("RGB")
        return im
    except DecodeError as e:
        raise ProblemException(
            400, "Bad encoding", "Image data must be base64 encoded"
        ) from e
    except UnidentifiedImageError as e:
        raise ProblemException(400, "Bad data", "Decoded data was not an image") from e


def find_lookalike(body: bytes):
    im = _deserialise_image(body)
    celebs = predictor.predict(im)

    return celebs, 200


connexion_app = FlaskApp(__name__, specification_dir=Path(__file__).parent)
connexion_app.add_api("spec.yaml", strict_validation=True)
connexion_app.add_error_handler(Exception, FlaskApp.common_error_handler)
CORS(connexion_app.app)  # TODO: only do this in dev for all origins

if __name__ == "__main__":
    connexion_app.run(port=5000)
else:
    app = connexion_app.app