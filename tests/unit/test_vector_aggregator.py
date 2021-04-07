import numpy as np

from index.builder import MedianVectorAggregator


def test_median_vector_aggregator():
    sut = MedianVectorAggregator()
    a = np.array([1.0, 1.0, 4.0])
    b = np.array([2.0, 2.0, 2.0])
    c = np.array([3.0, 3.0, 3.0])

    result = sut.aggregate([a, b, c])

    assert (result == np.array([2.0, 2.0, 3.0])).all()
