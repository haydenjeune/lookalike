import csv
import re
from typing import Iterable, Iterator, List, Generator

import boto3
from botocore.signers import generate_presigned_url
from bs4 import BeautifulSoup
from loguru import logger
import requests

from scraper.configuration import get_config

config = get_config()


class ImdbNameScraper:
    def __init__(self, gender: str, start_page: int = 1, end_page: int = -1) -> None:
        self.gender = gender
        self.end_page = end_page
        self.current_page = start_page

    @staticmethod
    def _get_page(gender: str, page_index: int) -> str:
        logger.info(f"Getting page {page_index}")
        start = (page_index * 50) + 1
        url = f"https://www.imdb.com/search/name/?gender={gender}&start={start}"
        # TODO: Handle errors
        response = requests.get(url)
        if not response.ok:
            raise RuntimeError(
                f"Received {response.status_code}: {response.text} calling {url}"
            )

        return response.text

    def __iter__(self) -> Iterator[List[str]]:
        return self

    def __next__(self) -> List[str]:
        if self.end_page != -1 and self.current_page > self.end_page:
            raise StopIteration()

        page = self._get_page(self.gender, self.current_page)
        self.current_page += 1

        page = BeautifulSoup(page, "html.parser")
        names = [
            str(element.find("a", {"href": re.compile("^/name/")}).string).strip()
            for element in page.find_all("h3", {"class": "lister-item-header"})
        ]

        return names


def batcher(iterable: Iterable, n: int = 10):
    args = [iter(iterable)] * n
    return zip(*args)


if __name__ == "__main__":
    sqs = boto3.resource("sqs")
    queue = sqs.Queue(config.EXTRACTION_QUEUE_URL)

    for names in ImdbNameScraper("female", 0, 99):
        for batch in batcher(names, n=10):
            logger.info(f"Sending batch {batch}")
            queue.send_messages(
                Entries=[
                    {
                        "Id": str(i),
                        "MessageBody": name,
                    }
                    for i, name in enumerate(batch)
                ]
            )
