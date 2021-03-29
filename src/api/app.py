import connexion
from PIL import Image
from io import BytesIO


def ping():
    return "pong"


def find_lookalike(body: bytes):
    im = Image.open(BytesIO(body)).convert("RGB")
    return {"celeb": "test"}, 200


app = connexion.FlaskApp(__name__)
app.add_api("spec.yaml", strict_validation=True)
app.run(port=8080)