import connexion
from PIL import Image
from io import BytesIO
from pathlib import Path

from api import configuration
from index.predictor import FaceNetDotProductPredictor
from index.storage import VectorIndex

config = configuration.get()
predictor = FaceNetDotProductPredictor(index=VectorIndex(config.vector_index_filepath))


def ping():
    return "pong"


def find_lookalike(body: bytes):
    im = Image.open(BytesIO(body)).convert("RGB")
    celebs = predictor.predict(im)
    return celebs, 200


connexion_app = connexion.FlaskApp(__name__, specification_dir=Path(__file__).parent)
connexion_app.add_api("spec.yaml", strict_validation=True)
connexion_app.add_error_handler(Exception, connexion.FlaskApp.common_error_handler)


if __name__ == "__main__":
    connexion_app.run(port=5000)
else:
    app = connexion_app.app