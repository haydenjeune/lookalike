import pytest
import mock
from PIL import Image
from io import BytesIO
from pathlib import Path
from base64 import b64encode
import api.app as app
from connexion import ProblemException
from index.predictor import FaceNetDotProductPredictor


@pytest.fixture()
def non_b64_jpg_data():
    with open("tests/assets/my-profile.jpeg", "rb") as f:
        return f.read()


@pytest.fixture()
def b64_jpg_data(non_b64_jpg_data):
    return b64encode(non_b64_jpg_data)


@pytest.fixture()
def b64_non_image_data():
    return b64encode(b"abcdefghijklmnopqrstuvwxyz")


@pytest.fixture()
def decompression_bomb_data():
    with open("tests/assets/10K-decompression.jpeg", "rb") as f:
        data = f.read()
    return b64encode(data)


def test_post_throws_exception_with_unencoded_data(non_b64_jpg_data):
    with pytest.raises(ProblemException) as e:
        app.find_lookalike(non_b64_jpg_data)
    assert e.value.status == 400


def test_post_throws_exception_with_encoded_non_image_data(b64_non_image_data):
    with pytest.raises(ProblemException) as e:
        app.find_lookalike(b64_non_image_data)
    assert e.value.status == 400


def test_post_throws_exception_with_decompression_bomb(decompression_bomb_data):
    with pytest.raises(ProblemException) as e:
        app.find_lookalike(decompression_bomb_data)
    assert e.value.status == 422
