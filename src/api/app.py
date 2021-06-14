from base64 import b64decode
from binascii import Error as DecodeError
from io import BytesIO
from pathlib import Path

from connexion import FlaskApp, ProblemException
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError

from api import configuration
from lib.index.predictor import FaceNetDotProductPredictor
from lib.index.storage import VectorIndex

config = configuration.get()
predictor = FaceNetDotProductPredictor(index=VectorIndex(config.vector_index_filepath))


def ping():
    return "pong"


def find_lookalike(body: bytes):
    im = _deserialise_image(body)

    # check for decompression bombs
    if im.size[0] * im.size[1] > config.max_image_pixels:
        _raise_unprocessable_entity("Image exceeds allowed number of pixels")

    # remove any alpha layer
    im = im.convert("RGB")

    celebs = predictor.predict(im)

    return celebs, 200


def _deserialise_image(data: bytes) -> Image.Image:
    try:
        data = b64decode(data)
        im = Image.open(BytesIO(data))
        return im
    except DecodeError:
        _raise_bad_request("Image data must be base64 encoded")
    except UnidentifiedImageError:
        _raise_bad_request("Decoded data was not an image")


def _raise_bad_request(msg: str):
    raise ProblemException(400, "Bad Request", msg)


def _raise_unprocessable_entity(msg: str):
    raise ProblemException(422, "Unprocessable Entity", msg)


connexion_app = FlaskApp(__name__, specification_dir=Path(__file__).parent.resolve())
connexion_app.add_api("spec.yaml", strict_validation=True)
connexion_app.add_error_handler(Exception, FlaskApp.common_error_handler)
CORS(connexion_app.app)  # TODO: only do this in dev for all origins


if __name__ == "__main__":
    connexion_app.run(port=5000)
else:
    app = connexion_app.app