from loguru import logger

import grpc

from lib.index.index_pb2 import IndexSearch
from lib.index.index_pb2_grpc import IndexStub


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = IndexStub(channel)
        response = stub.Search(IndexSearch(vector=b"test", num_results=5))
    logger.info("Greeter client received:\n" + str(response))


if __name__ == "__main__":
    run()