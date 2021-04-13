from typing import NamedTuple
import connexion
from PIL import Image
from io import BytesIO
from pathlib import Path
from flask_cors import CORS
import base64
from urllib.parse import quote

from api import configuration
from index.predictor import FaceNetDotProductPredictor
from index.storage import VectorIndex

config = configuration.get()
predictor = FaceNetDotProductPredictor(index=VectorIndex(config.vector_index_filepath))


def ping():
    return "pong"


def find_lookalike(body: bytes):
    body = base64.b64decode(body)
    im = Image.open(BytesIO(body)).convert("RGB")
    celebs = predictor.predict(im)
    response = [
        {
            "name": c.name,
            "similarity": c.similarity,
            "image": quote(f"/Users/hayden.jeune/.celebstore/images/{c.name}/0.jpg"),
        }
        for c in celebs
    ]
    return response, 200


connexion_app = connexion.FlaskApp(__name__, specification_dir=Path(__file__).parent)
connexion_app.add_api("spec.yaml", strict_validation=True)
connexion_app.add_error_handler(Exception, connexion.FlaskApp.common_error_handler)
CORS(connexion_app.app)  # TODO: only do this in dev for all origins

if __name__ == "__main__":
    connexion_app.run(port=5000)
else:
    app = connexion_app.app