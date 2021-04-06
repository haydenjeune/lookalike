import connexion
from PIL import Image
from io import BytesIO

from src.api import configuration
from src.index.predictor import FaceNetDotProductPredictor
from src.index.storage import VectorIndex

config = configuration.get()
predictor = FaceNetDotProductPredictor(index=VectorIndex(config.vector_index_filepath))


def ping():
    return "pong"


def find_lookalike(body: bytes):
    im = Image.open(BytesIO(body)).convert("RGB")
    celebs = predictor.predict(im)
    return celebs, 200


connexion_app = connexion.FlaskApp(__name__)
connexion_app.add_api("spec.yaml", strict_validation=True)

if __name__ == "__main__":
    connexion_app.run(port=8080)
else:
    app = connexion_app.app