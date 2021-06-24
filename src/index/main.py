from concurrent import futures
from io import BytesIO

import grpc
from loguru import logger
from numpy import load

from index.configuration import get_config
from index.generated.index_pb2 import IndexResults, Celebrity
from index.generated.index_pb2_grpc import IndexServicer, add_IndexServicer_to_server
from lib.index.faiss import FaissIndex

config = get_config()


class IndexService(IndexServicer):
    """IndexService is the Server for the vector similarity search over gRPC"""

    def __init__(self):
        super().__init__()
        self.faiss_index = FaissIndex(
            config.INDEX_VECTOR_DIMENSIONS, from_dir=config.INDEX_ROOT
        )

    def Search(self, request, context):
        vec = load(BytesIO(request.vector), allow_pickle=False)

        return IndexResults(
            celebrities=[
                Celebrity(name=name, similarity=similarity)
                for name, similarity in self.faiss_index.search(
                    vec, request.num_results
                )
            ]
        )


def serve():
    # Faiss search releases GIL so threadpool allows use of multi cores
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=config.MAX_WORKERS))
    add_IndexServicer_to_server(IndexService(), server)
    server.add_insecure_port(config.ADDRESS)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logger.info("Starting Index Service")
    serve()