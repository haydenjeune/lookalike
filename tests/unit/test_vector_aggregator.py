import numpy as np
from math import sqrt

from lib.vector.aggregator import MedianVectorAggregator


def test_median_vector_aggregator():
    sut = MedianVectorAggregator()
    a = np.array([11.0, 3.0, 4.0])
    b = np.array([12.0, 4.0, 2.0])
    c = np.array([13.0, 5.0, 3.0])
    expected = np.array([12.0 / 13.0, 4.0 / 13.0, 3.0 / 13])
    # expected is normalised.
    # note: test relies on 3**2 + 4**2 + 12**2 = 13**2

    result = sut.aggregate([a, b, c])
    print(result, expected)
    assert (result == expected).all()
