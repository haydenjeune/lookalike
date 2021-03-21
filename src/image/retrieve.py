from abc import ABC, abstractmethod
from dataclasses import dataclass
import io
import logging
from urllib.parse import quote

from bs4 import BeautifulSoup
from PIL import Image
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
    def retrieve(self, name: str) -> Image:
        pass


@dataclass
class WikipediaImageRetriever(ImageRetriever):
    """
    Tries to fetch an image from wikipedia for a given name.

    I'd love to use Google Images but it's robots.txt doesn't allow it :'(
    """

    _url: str = "https://en.wikipedia.org"
    _page_stem: str = "/wiki/"

    def retrieve(self, name: str) -> Image.Image:
        resp = requests.get(self._url + self._page_stem + self._encode_name(name))
        if resp.status_code == 404:
            raise NoPageException(f"No main page found at {resp.url}")

        try:
            image_page_url = self._find_image_page_url(resp.text)
        except InvalidInfoBoxException as e:
            raise ImageRetrieverException(f"Failed to process {name}: {str(e)}") from e

        # check for relative link
        if image_page_url.startswith("/"):
            image_page_url = self._url + image_page_url

        resp = requests.get(image_page_url)
        if resp.status_code == 404:
            raise NoPageException(f"No image page found at {resp.url}")
        image_url = self._find_full_image_url(resp.text)

        # check scheme has been specified, sometimes wikipedia specifies it like //host.com/image.jpg
        if not image_url.startswith("http") and image_url.startswith("//"):
            image_url = "https:" + image_url

        log.info(f"Downloading image from {image_url}")
        resp = requests.get(image_url, stream=True)
        return Image.open(io.BytesIO(resp.content))

    @staticmethod
    def _encode_name(name: str) -> str:
        return quote(name.replace(" ", "_"))

    @staticmethod
    def _find_image_page_url(html: str) -> str:
        page = BeautifulSoup(html, "html.parser")

        # find the infoboxes
        infoboxes = page.find_all("table", {"class": "infobox"})
        if len(infoboxes) > 1:
            raise InvalidInfoBoxException(
                f"Invalid assumption that the infobox class is unique. {len(infoboxes)} found"
            )
        elif len(infoboxes) == 0:
            raise InvalidInfoBoxException("No infoboxes found")

        # get the biggest image in the infobox
        imgs = infoboxes[0].find_all("img")
        if len(imgs) == 0:
            raise InvalidInfoBoxException("No images found in the infobox")

        def get_img_size(img) -> int:
            width = int(img.get("width", 0))
            height = int(img.get("height", 0))
            return width * height

        img = max(imgs, key=get_img_size)

        # return the parent link
        return img.parent["href"]

    @staticmethod
    def _find_full_image_url(html: str) -> str:
        page = BeautifulSoup(html, "html.parser")
        divs = page.find_all("div", {"class": "fullImageLink", "id": "file"})
        if len(divs) != 1:
            raise InvalidImagePageException("Expected a single main image")

        return divs[0].a["href"]
