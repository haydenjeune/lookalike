import pytest
from src.celebrity.finder import UrlCelebrityListFinder


def test_simple():
    finder = UrlCelebrityListFinder()
    assert True