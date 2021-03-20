from abc import ABC, abstractmethod
from dataclasses import dataclass
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


class InvalidInfoBoxesException(ImageRetrieverException):
    pass


class ImageRetriver(ABC):
    @abstractmethod
    def retrieve(self, name: str) -> Image:
        pass


@dataclass
class WikipediaImageRetriver(ImageRetriver):
    """
    Tries to fetch an image from wikipedia for a given name.

    I'd love to use Google Images but it's robots.txt doesn't allow it :'(
    """

    _url: str = "https://en.wikipedia.org"
    _page_stem: str = "/wiki/"

    def retrieve(self, name: str) -> Image:
        resp = requests.get(self._url + self._page_stem + self._encode_name(name))
        if resp.status_code == 400:
            raise NoPageException("No")
        image_page_url = self._find_image_page_url(resp.text)
        print(image_page_url)
        return Image()

    @staticmethod
    def _encode_name(name: str) -> str:
        return quote(name.replace(" ", "_"))

    @staticmethod
    def _find_image_page_url(html: str) -> str:
        page = BeautifulSoup(html, "html.parser")

        # find the infoboxes
        infoboxes = page.find_all("table", {"class": "infobox"})
        if len(infoboxes) > 1:
            raise InvalidInfoBoxesException(f"Invalid assumption that the infobox class is unique. {len(infoboxes)} found")
        elif len(infoboxes) == 0:
            raise InvalidInfoBoxesException("No infoboxes found")

        # get the biggest image in the infobox
        imgs = infoboxes[0].find_all("img")
        if len(imgs) == 0:
            raise NoImageException("No images found in the infobox")
        def get_img_size(img) -> int:
            width = int(img.get("width", 0))
            height = int(img.get("height", 0))
            return width * height
        img = max(imgs, key=get_img_size)

        # return the parent link
        return img.parent["href"]

