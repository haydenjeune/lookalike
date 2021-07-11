from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import BytesIO
from urllib.parse import quote
from typing import Iterable, Optional, Tuple

from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError
import requests
from loguru import logger


VALID_EXTENSIONS = {"png", "jpg", "jpeg"}


class ImageRetrieverException(Exception):
    pass


class ImageRetriever(ABC):
    @abstractmethod
    def retrieve(self, name: str, max_images=None) -> Iterable[Tuple[Image.Image, str]]:
        pass


@dataclass
class WikipediaImageRetriever(ImageRetriever):
    """
    Tries to fetch an image from wikipedia for a given name.

    I'd love to use Google Images but it's robots.txt doesn't allow it :'(
    """

    _url: str = "https://en.wikipedia.org"
    _page_stem: str = "/wiki/"

    def retrieve(self, name: str, max_images=None) -> Iterable[Tuple[Image.Image, str]]:
        resp = requests.get(self._url + self._page_stem + self._encode_name(name))
        if resp.status_code == 404:
            raise ImageRetrieverException(f"No main page found at {resp.url}")

        image_page_urls = self._find_image_page_urls(resp.text)

        retrieved = 0
        for url in image_page_urls:
            if max_images and retrieved >= max_images:
                return

            resp = requests.get(url)
            if resp.status_code == 404:
                logger.error(f"HTTP 404, couldn't get {url}")
            else:
                try:
                    image_url = self._find_full_image_url(resp.text)
                    if (
                        not image_url
                        or image_url.split(".")[-1].lower() not in VALID_EXTENSIONS
                    ):
                        continue
                    resp = requests.get(
                        image_url,
                        stream=True,
                        headers={"user-agent": "Lookalike/0.1 (hejeune@gmail.com)"},
                    )
                    # TODO: Handle 429 and split out a singleton wikipedia client to rate limit
                    retrieved += 1
                    yield Image.open(BytesIO(resp.content)).convert("RGB"), image_url
                except UnidentifiedImageError as e:
                    logger.warning(f"Received bad image data for {url}", exc_info=e)

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
    def _find_full_image_url(html: str) -> Optional[str]:
        page = BeautifulSoup(html, "html.parser")
        divs = page.find_all("div", {"class": "fullImageLink", "id": "file"})
        if len(divs) == 0:
            return None

        image_url = divs[0].a["href"]
        # check scheme has been specified, sometimes wikipedia specifies it like //host.com/image.jpg
        if not image_url.startswith("http") and image_url.startswith("//"):
            image_url = "https:" + image_url

        return image_url
