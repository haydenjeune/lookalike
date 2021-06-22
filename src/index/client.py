import atexit
from io import BytesIO
from dataclasses import dataclass
from typing import List

import grpc
from numpy import ndarray, save

from index.generated.index_pb2_grpc import IndexStub
from index.generated.index_pb2 import IndexSearch


@dataclass
class SearchResult:
    name: str
    similarity: float


class IndexClient:
    """IndexClient allows remote vector similarity lookup over gRPC"""

    def __init__(self, remote_addr: str):
        # use a secure channel
        channel = grpc.insecure_channel(remote_addr)
        atexit.register(channel.close)
        self.stub = IndexStub(channel)

    def search(self, vec: ndarray, num_results: int = 5) -> List[SearchResult]:
        data_bytes = BytesIO()
        save(data_bytes, vec, allow_pickle=False)

        request = IndexSearch(vector=data_bytes.getvalue(), num_results=num_results)
        response = self.stub.Search(request)

        return [
            SearchResult(celeb.name, celeb.similarity) for celeb in response.celebrities
        ]
