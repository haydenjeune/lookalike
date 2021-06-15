from random import shuffle

import mock
import numpy as np
import pytest
from PIL.Image import Image

from lib.index.builder import FaceNetPyTorchImageVectoriser
from lib.index.predictor import top_k, FaceNetDotProductPredictor
from lib.index.storage import VectorIndex

# run multiple times to catch randomness
@pytest.mark.parametrize("execution_number", range(100))
def test_top_k_finds_top_k_values(execution_number):
    vals = list(range(100))
    shuffle(vals)

    top = top_k(vals, k=3, key=lambda x: x)

    assert set(top) == {97, 98, 99}


def test_top_k_handles_k_gt_len_items():
    vals = [1, 2, 3]
    top = top_k(vals, k=4, key=lambda x: x)
    assert set(top) == {1, 2, 3}


def test_top_k_handles_structured_input():
    vals = [
        {"num": 4.0, "as_string": "four"},
        {"num": 1.0, "as_string": "one"},
        {"num": 3.0, "as_string": "three"},
        {"num": 2.0, "as_string": "two"},
        {"num": 5.0, "as_string": "five"},
    ]
    shuffle(vals)

    top = top_k(vals, k=3, key=lambda x: x["num"])

    assert {item["num"] for item in top} == {3.0, 4.0, 5.0}
    assert {item["as_string"] for item in top} == {"three", "four", "five"}


@pytest.fixture
def mock_index():
    vectors = [
        ("one", np.array([0.0, 1.0, 0.0, 0.0])),
        ("two", np.array([0.0, 0.0, 1.0, 0.0])),
        ("three", np.array([0.0, 0.0, 0.0, 1.0])),
        ("four", np.array([1.0, 0.0, 0.0, 0.0])),
    ]
    index = mock.create_autospec(VectorIndex, instance=True)
    type(index).vectors = mock.PropertyMock(return_value=vectors)
    return index


def test_predict_returns_expected_result(
    mock_index: VectorIndex,
):
    vectoriser = mock.create_autospec(FaceNetPyTorchImageVectoriser, instance=True)
    vectoriser.vectorise = mock.Mock(return_value=np.array([0.0, 0.0, 1.0, 1.0]))

    sut = FaceNetDotProductPredictor(
        index=mock_index, vectoriser=vectoriser, num_results=2
    )
    result = sut.predict(Image())
    assert {r.name for r in result} == {"two", "three"}


def test_predict_returns_expected_result_with_unvectorisable_image(
    mock_index: VectorIndex,
):
    vectoriser = mock.create_autospec(FaceNetPyTorchImageVectoriser, instance=True)
    vectoriser.vectorise = mock.Mock(return_value=None)

    sut = FaceNetDotProductPredictor(
        index=mock_index, vectoriser=vectoriser, num_results=2
    )

    result = sut.predict(Image())

    assert result == []
