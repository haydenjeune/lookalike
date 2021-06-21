from concurrent import futures

import grpc
from loguru import logger

from lib.index.index_pb2 import IndexSearch, IndexResults, Celebrity
from lib.index.index_pb2_grpc import IndexServicer, add_IndexServicer_to_server


class IndexService(IndexServicer):
    def Search(self, request, context):
        return IndexResults(
            celebrities=[
                Celebrity(name="Test Celeb", similarity=1.0)
                for _ in range(request.num_results)
            ]
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_IndexServicer_to_server(IndexService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logger.info("Starting Index Service")
    serve()