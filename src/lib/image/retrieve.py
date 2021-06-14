from abc import ABC, abstractmethod
from dataclasses import dataclass
import io
import logging
from sys import exc_info
from urllib.parse import quote
from typing import Iterable

from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError
import requests

log = logging.getLogger(__name__)


class ImageRetrieverException(Exception):
    pass


class NoPageException(ImageRetrieverException):
    pass


class NoImageException(ImageRetrieverException):
    pass


class InvalidInfoBoxException(ImageRetrieverException):
    pass


class InvalidImagePageException(ImageRetrieverException):
    pass


class ImageRetriever(ABC):
    @abstractmethod
    def retrieve(self, name: str, max_images=None) -> Iterable[Image.Image]:
        pass


@dataclass
class WikipediaImageRetriever(ImageRetriever):
    """
    Tries to fetch an image from wikipedia for a given name.

    I'd love to use Google Images but it's robots.txt doesn't allow it :'(
    """

    _url: str = "https://en.wikipedia.org"
    _page_stem: str = "/wiki/"

    def retrieve(self, name: str, max_images=None) -> Iterable[Image.Image]:
        resp = requests.get(self._url + self._page_stem + self._encode_name(name))
        if resp.status_code == 404:
            raise NoPageException(f"No main page found at {resp.url}")

        image_page_urls = self._find_image_page_urls(resp.text)

        retrieved = 0
        for url in image_page_urls:
            if max_images and retrieved >= max_images:
                return

            resp = requests.get(url)
            if resp.status_code == 404:
                log.warning(f"HTTP 404, couldn't get {url}")
            else:
                try:
                    image_url = self._find_full_image_url(resp.text)
                    if image_url.split(".")[-1].lower() not in {"png", "jpg", "jpeg"}:
                        continue
                    resp = requests.get(image_url, stream=True)
                    retrieved += 1
                    yield Image.open(io.BytesIO(resp.content)).convert("RGB")
                except UnidentifiedImageError as e:
                    log.exception(f" {url}", exc_info=e)
                except ImageRetrieverException as e:
                    log.exception(f"Failed to get main image from {url}", exc_info=e)

    @staticmethod
    def _encode_name(name: str) -> str:
        return quote(name.replace(" ", "_"))

    def _find_image_page_urls(self, html: str) -> Iterable[str]:
        page = BeautifulSoup(html, "html.parser")

        image_links = page.find_all("a", {"class": "image"})
        if len(image_links) == 0:
            return

        for link in image_links:
            image_page_url = link["href"]

            # check for relative links
            if image_page_url.startswith("/"):
                image_page_url = self._url + image_page_url

            yield image_page_url

    @staticmethod
    def _find_full_image_url(html: str) -> str:
        page = BeautifulSoup(html, "html.parser")
        divs = page.find_all("div", {"class": "fullImageLink", "id": "file"})
        if len(divs) != 1:
            raise InvalidImagePageException("Expected a single main image")

        image_url = divs[0].a["href"]
        # check scheme has been specified, sometimes wikipedia specifies it like //host.com/image.jpg
        if not image_url.startswith("http") and image_url.startswith("//"):
            image_url = "https:" + image_url

        return image_url
