from base64 import b64encode

from connexion import ProblemException
import pytest
import numpy as np

from api import app
from index.client import SearchResult


@pytest.fixture()
def vector():
    return np.random.rand(512)


@pytest.fixture()
def search_results():
    return [SearchResult("test one", 0.5)]


@pytest.fixture()
def vectoriser(mocker, vector):
    mocker.patch("api.app.FaceNetPyTorchImageVectoriser.vectorise", return_value=vector)


@pytest.fixture()
def empty_vectoriser(mocker):
    mocker.patch("api.app.FaceNetPyTorchImageVectoriser.vectorise", return_value=None)


@pytest.fixture()
def index_service(mocker, search_results):
    mocker.patch("api.app.IndexClient.search", return_value=search_results)


@pytest.fixture()
def empty_index_service(mocker):
    mocker.patch("api.app.IndexClient.search", return_value=[])


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


def test_post_jpeg(vectoriser, index_service, search_results, b64_jpg_data):
    response = app.find_lookalike(b64_jpg_data)
    assert response == (search_results, 200)


def test_post_no_prediction(empty_vectoriser, index_service, b64_jpg_data):
    response = app.find_lookalike(b64_jpg_data)
    assert response == ([], 200)
