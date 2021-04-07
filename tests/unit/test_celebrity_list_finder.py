import pytest
import requests_mock

from celebrity.finder import UrlCelebrityListFinder


@pytest.fixture
def mock_celeb_url():
    with requests_mock.Mocker() as m:
        m.get(
            "http://test.com",
            text="\n\nHayden Jeune\nUnïcõdé Ñámę \t\n\nAnother Name\n\n   \n\n",
        )
        yield


def test_find_returns_cleaned_list(mock_celeb_url):
    finder = UrlCelebrityListFinder(list_url="http://test.com")

    result = finder.find()

    assert result == ["Hayden Jeune", "Unïcõdé Ñámę", "Another Name"]