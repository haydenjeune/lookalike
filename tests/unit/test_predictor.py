from random import shuffle

import pytest

from index.predictor import top_k

# run multiple times to catch randomness
@pytest.mark.parametrize("execution_number", range(100))
def test_top_k_finds_top_k_values(execution_number):
    vals = list(range(100))
    shuffle(vals)

    top = top_k(vals, k=3, key=lambda x: x)

    assert set(top) == {97, 98, 99}


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
